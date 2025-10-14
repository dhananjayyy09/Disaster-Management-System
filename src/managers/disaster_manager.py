"""
Disaster Management Module
Handles disaster-related operations and data validation
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from database_manager import DatabaseManager

class DisasterManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def create_disaster(self, name: str, disaster_type: str, location: str, 
                       severity: str, description: str = "") -> Dict:
        """Create a new disaster record"""
        try:
            # Validate inputs
            if not name or not disaster_type or not location or not severity:
                return {"success": False, "message": "All required fields must be filled"}
            
            # Validate disaster type
            valid_types = ['Earthquake', 'Flood', 'Wildfire', 'Hurricane', 'Tornado', 'Other']
            if disaster_type not in valid_types:
                return {"success": False, "message": f"Invalid disaster type. Must be one of: {', '.join(valid_types)}"}
            
            # Validate severity
            valid_severities = ['Low', 'Medium', 'High', 'Critical']
            if severity not in valid_severities:
                return {"success": False, "message": f"Invalid severity. Must be one of: {', '.join(valid_severities)}"}
            
            # Create disaster
            start_date = date.today().strftime('%Y-%m-%d')
            success = self.db.add_disaster(name, disaster_type, location, severity, start_date, description)
            
            if success:
                return {"success": True, "message": f"Disaster '{name}' created successfully"}
            else:
                return {"success": False, "message": "Failed to create disaster"}
                
        except Exception as e:
            return {"success": False, "message": f"Error creating disaster: {str(e)}"}
    
    def get_disasters_summary(self) -> List[Dict]:
        """Get summary of all disasters with camp counts"""
        disasters = self.db.get_all_disasters()
        
        for disaster in disasters:
            # Get camp count for each disaster
            camps = self.db.get_camps_by_disaster(disaster['disaster_id'])
            disaster['camp_count'] = len(camps)
            
            # Calculate days since start
            start_date = disaster['start_date']
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
            elif hasattr(start_date, 'date'):
                start_date = start_date.date()
            days_active = (datetime.now().date() - start_date).days
            disaster['days_active'] = days_active
            
        return disasters
    
    def update_disaster_status(self, disaster_id: int, status: str) -> Dict:
        """Update disaster status"""
        try:
            valid_statuses = ['Active', 'Resolved', 'Ongoing']
            if status not in valid_statuses:
                return {"success": False, "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
            
            success = self.db.update_disaster_status(disaster_id, status)
            
            if success:
                return {"success": True, "message": f"Disaster status updated to '{status}'"}
            else:
                return {"success": False, "message": "Failed to update disaster status"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating disaster status: {str(e)}"}
    
    def get_disaster_details(self, disaster_id: int) -> Optional[Dict]:
        """Get detailed information about a specific disaster"""
        disasters = self.db.get_all_disasters()
        disaster = next((d for d in disasters if d['disaster_id'] == disaster_id), None)
        
        if disaster:
            # Get associated camps
            camps = self.db.get_camps_by_disaster(disaster_id)
            disaster['camps'] = camps
            
            # Get total occupancy across all camps
            total_occupancy = sum(camp['current_occupancy'] for camp in camps)
            total_capacity = sum(camp['capacity'] for camp in camps)
            disaster['total_occupancy'] = total_occupancy
            disaster['total_capacity'] = total_capacity
            disaster['occupancy_percentage'] = (total_occupancy / total_capacity * 100) if total_capacity > 0 else 0
            
        return disaster
    
    def get_active_disasters_count(self) -> int:
        """Get count of active disasters"""
        disasters = self.db.get_all_disasters()
        return len([d for d in disasters if d['status'] == 'Active'])
    
    def get_disaster_statistics(self) -> Dict:
        """Get disaster statistics for dashboard"""
        disasters = self.db.get_all_disasters()
        
        stats = {
            'total_disasters': len(disasters),
            'active_disasters': len([d for d in disasters if d['status'] == 'Active']),
            'resolved_disasters': len([d for d in disasters if d['status'] == 'Resolved']),
            'by_type': {},
            'by_severity': {}
        }
        
        # Count by type
        for disaster in disasters:
            disaster_type = disaster['disaster_type']
            severity = disaster['severity']
            
            stats['by_type'][disaster_type] = stats['by_type'].get(disaster_type, 0) + 1
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
            
        return stats
