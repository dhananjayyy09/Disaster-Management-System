"""
Relief Camp Management Module
Handles camp-related operations and resource allocation
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from database_manager import DatabaseManager


class CampManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def create_camp(self, name: str, disaster_id: int, location: str, 
                   capacity: int, contact_person: str = "", contact_phone: str = "") -> Dict:
        """Create a new relief camp"""
        try:
            # Validate inputs
            if not name or not location or capacity <= 0:
                return {"success": False, "message": "Camp name, location, and capacity are required"}
            
            # Check if disaster exists
            disasters = self.db.get_all_disasters()
            disaster = next((d for d in disasters if d['disaster_id'] == disaster_id), None)
            if not disaster:
                return {"success": False, "message": "Invalid disaster selected"}
            
            # Create camp
            success = self.db.add_camp(name, disaster_id, location, capacity, contact_person, contact_phone)
            
            if success:
                return {"success": True, "message": f"Camp '{name}' created successfully"}
            else:
                return {"success": False, "message": "Failed to create camp"}
                
        except Exception as e:
            return {"success": False, "message": f"Error creating camp: {str(e)}"}
    
    def get_camps_summary(self) -> List[Dict]:
        """Get summary of all camps with additional info"""
        camps = self.db.get_all_camps()
        
        for camp in camps:
            # Calculate occupancy percentage
            occupancy_pct = (camp.get('current_occupancy', 0) / camp.get('capacity', 1) * 100) if camp.get('capacity', 0) > 0 else 0
            camp['occupancy_percentage'] = round(occupancy_pct, 1)
            
            # Determine status based on occupancy
            if occupancy_pct >= 95:
                camp['capacity_status'] = 'Overcrowded'
            elif occupancy_pct >= 80:
                camp['capacity_status'] = 'Near Capacity'
            elif occupancy_pct >= 50:
                camp['capacity_status'] = 'Moderate'
            else:
                camp['capacity_status'] = 'Low'
            
            # Get resource shortages for this camp
            resources = self.db.get_camp_resources(camp['camp_id'])
            shortages = [r for r in resources if r.get('quantity_needed', 0) > r.get('quantity_available', 0)]
            camp['resource_shortages'] = len(shortages)
            
        return camps
    
    def update_camp_occupancy(self, camp_id: int, new_occupancy: int) -> Dict:
        """Update camp occupancy"""
        try:
            # Get camp info
            camps = self.db.get_all_camps()
            camp = next((c for c in camps if c['camp_id'] == camp_id), None)
            
            if not camp:
                return {"success": False, "message": "Camp not found"}
            
            if new_occupancy < 0 or new_occupancy > camp.get('capacity', 0):
                return {"success": False, "message": f"Occupancy must be between 0 and {camp.get('capacity', 0)}"}
            
            success = self.db.update_camp_occupancy(camp_id, new_occupancy)
            
            if success:
                return {"success": True, "message": f"Camp occupancy updated to {new_occupancy}"}
            else:
                return {"success": False, "message": "Failed to update camp occupancy"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating occupancy: {str(e)}"}
    
    def get_camp_details(self, camp_id: int) -> Optional[Dict]:
        """Get detailed information about a specific camp"""
        camps = self.db.get_all_camps()
        camp = next((c for c in camps if c['camp_id'] == camp_id), None)
        
        if camp:
            # Get resources for this camp
            resources = self.db.get_camp_resources(camp_id)
            camp['resources'] = resources
            
            # Get volunteer assignments
            volunteers = self.db.execute_query(
                "SELECT va.*, v.first_name, v.last_name, v.skills FROM volunteer_assignments va "
                "JOIN volunteers v ON va.volunteer_id = v.volunteer_id "
                "WHERE va.camp_id = %s AND va.status = 'Active'",
                (camp_id,)
            )
            camp['volunteers'] = volunteers
            
            # Calculate resource statistics
            total_shortages = sum(1 for r in resources if r.get('quantity_needed', 0) > r.get('quantity_available', 0))
            camp['total_shortages'] = total_shortages
            
            # Calculate days since creation
            try:
                created_date_str = camp.get('created_at', '')
                if created_date_str:
                    if ' ' in str(created_date_str):
                        created_date = datetime.strptime(str(created_date_str), '%Y-%m-%d %H:%M:%S')
                    else:
                        created_date = datetime.strptime(str(created_date_str), '%Y-%m-%d')
                    
                    days_active = (datetime.now() - created_date).days
                    camp['days_active'] = days_active
                else:
                    camp['days_active'] = 0
            except Exception as e:
                print(f"Error parsing camp date: {e}")
                camp['days_active'] = 0
            
        return camp
    
    def get_overcrowded_camps(self) -> List[Dict]:
        """Get camps that are overcrowded (>95% capacity)"""
        camps = self.db.get_all_camps()
        overcrowded = []
        
        for camp in camps:
            capacity = camp.get('capacity', 0)
            occupancy = camp.get('current_occupancy', 0)
            occupancy_pct = (occupancy / capacity * 100) if capacity > 0 else 0
            
            if occupancy_pct > 95:
                camp['occupancy_percentage'] = round(occupancy_pct, 1)
                overcrowded.append(camp)
                
        return overcrowded
    
    def get_camps_needing_resources(self) -> List[Dict]:
        """Get camps with resource shortages"""
        camps = self.db.get_all_camps()
        needy_camps = []
        
        for camp in camps:
            resources = self.db.get_camp_resources(camp['camp_id'])
            shortages = [r for r in resources if r.get('quantity_needed', 0) > r.get('quantity_available', 0)]
            
            if shortages:
                camp['resource_shortages'] = shortages
                camp['shortage_count'] = len(shortages)
                needy_camps.append(camp)
                
        return needy_camps
    
    def get_camp_statistics(self) -> Dict:
        """Get camp statistics for dashboard"""
        camps = self.db.get_all_camps()
        active_camps = [c for c in camps if c.get('status') == 'Active']
        
        if not active_camps:
            return {
                'total_camps': 0,
                'active_camps': 0,
                'total_capacity': 0,
                'total_occupancy': 0,
                'average_occupancy': 0,
                'overcrowded_camps': 0
            }
        
        total_capacity = sum(camp.get('capacity', 0) for camp in active_camps)
        total_occupancy = sum(camp.get('current_occupancy', 0) for camp in active_camps)
        average_occupancy = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
        
        overcrowded_count = len([c for c in active_camps 
                                if c.get('capacity', 0) > 0 and 
                                (c.get('current_occupancy', 0) / c.get('capacity', 1) * 100) > 95])
        
        return {
            'total_camps': len(camps),
            'active_camps': len(active_camps),
            'total_capacity': total_capacity,
            'total_occupancy': total_occupancy,
            'average_occupancy': round(average_occupancy, 1),
            'overcrowded_camps': overcrowded_count
        }
