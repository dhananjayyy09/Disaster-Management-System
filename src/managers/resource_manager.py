"""
Resource Management Module
Handles resource tracking, allocation, and shortage detection
"""

from typing import List, Dict, Optional
from database_manager import DatabaseManager

class ResourceManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def get_resource_shortages(self) -> List[Dict]:
        """Get all resources with shortages"""
        return self.db.get_resource_shortages()
    
    def get_critical_shortages(self) -> List[Dict]:
        """Get resources with critical shortages (needed > 2 * available)"""
        shortages = self.get_resource_shortages()
        critical = []
        
        for shortage in shortages:
            available = shortage['quantity_available']
            needed = shortage['quantity_needed']
            
            # Critical if needed is more than double available
            if needed > (available * 2):
                shortage['shortage_ratio'] = round(needed / available, 2) if available > 0 else float('inf')
                shortage['shortage_severity'] = 'Critical'
                critical.append(shortage)
            elif needed > (available * 1.5):
                shortage['shortage_ratio'] = round(needed / available, 2) if available > 0 else float('inf')
                shortage['shortage_severity'] = 'High'
                critical.append(shortage)
                
        return critical
    
    def update_resource_quantities(self, resource_id: int, available: int, needed: int) -> Dict:
        """Update resource quantities"""
        try:
            if available < 0 or needed < 0:
                return {"success": False, "message": "Quantities cannot be negative"}
            
            success = self.db.update_resource_quantity(resource_id, available, needed)
            
            if success:
                return {"success": True, "message": "Resource quantities updated successfully"}
            else:
                return {"success": False, "message": "Failed to update resource quantities"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating resources: {str(e)}"}
    
    def allocate_donation_to_camp(self, donation_id: int, camp_id: int, quantity: int) -> Dict:
        """Allocate donation to specific camp"""
        try:
            # Get donation details
            donations = self.db.get_all_donations()
            donation = next((d for d in donations if d['donation_id'] == donation_id), None)
            
            if not donation:
                return {"success": False, "message": "Donation not found"}
            
            if quantity > donation['quantity_donated']:
                return {"success": False, "message": "Allocation quantity exceeds donation amount"}
            
            # Create allocation record
            success = self.db.allocate_donation(donation_id, camp_id, quantity)
            
            if success:
                # Update donation status if fully allocated
                remaining = donation['quantity_donated'] - quantity
                if remaining <= 0:
                    self.db.execute_update(
                        "UPDATE donations SET status = 'Allocated' WHERE donation_id = %s",
                        (donation_id,)
                    )
                
                return {"success": True, "message": f"Successfully allocated {quantity} units to camp"}
            else:
                return {"success": False, "message": "Failed to allocate donation"}
                
        except Exception as e:
            return {"success": False, "message": f"Error allocating donation: {str(e)}"}
    
    def auto_allocate_donations(self) -> Dict:
        """Automatically allocate donations to camps with shortages"""
        try:
            allocations_made = 0
            
            # Get all pending donations
            donations = [d for d in self.db.get_all_donations() if d['status'] == 'Pending']
            
            for donation in donations:
                resource_type_id = donation['resource_type_id']
                quantity_available = donation['quantity_donated']
                
                # Find camps with shortages for this resource type
                shortages = self.get_resource_shortages()
                relevant_shortages = [s for s in shortages if s['resource_type_id'] == resource_type_id]
                
                # Sort by shortage severity (needed - available)
                relevant_shortages.sort(key=lambda x: x['quantity_needed'] - x['quantity_available'], reverse=True)
                
                # Allocate to camps with highest need first
                for shortage in relevant_shortages:
                    if quantity_available <= 0:
                        break
                    
                    needed = shortage['quantity_needed'] - shortage['quantity_available']
                    allocate_amount = min(quantity_available, needed)
                    
                    if allocate_amount > 0:
                        success = self.allocate_donation_to_camp(
                            donation['donation_id'], 
                            shortage['camp_id'], 
                            allocate_amount
                        )
                        
                        if success['success']:
                            allocations_made += 1
                            quantity_available -= allocate_amount
            
            return {
                "success": True, 
                "message": f"Auto-allocation completed. {allocations_made} allocations made."
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error in auto-allocation: {str(e)}"}
    
    def get_resource_statistics(self) -> Dict:
        """Get resource statistics for dashboard"""
        stats = {
            'total_resource_types': 0,
            'total_shortages': 0,
            'critical_shortages': 0,
            'resources_by_type': {},
            'top_shortages': []
        }
        
        # Get resource types
        resource_types = self.db.get_resource_type_list()
        stats['total_resource_types'] = len(resource_types)
        
        # Get shortages
        shortages = self.get_resource_shortages()
        stats['total_shortages'] = len(shortages)
        
        # Get critical shortages
        critical = self.get_critical_shortages()
        stats['critical_shortages'] = len(critical)
        
        # Count shortages by resource type
        for shortage in shortages:
            type_name = shortage['type_name']
            if type_name not in stats['resources_by_type']:
                stats['resources_by_type'][type_name] = 0
            stats['resources_by_type'][type_name] += 1
        
        # Get top 5 shortages by quantity
        top_shortages = sorted(shortages, 
                             key=lambda x: x['quantity_needed'] - x['quantity_available'], 
                             reverse=True)[:5]
        stats['top_shortages'] = top_shortages
        
        return stats
    
    def get_donation_allocation_summary(self) -> List[Dict]:
        """Get summary of donation allocations"""
        query = """
        SELECT da.*, d.donor_name, d.quantity_donated, rt.type_name, c.camp_name
        FROM donation_allocations da
        JOIN donations d ON da.donation_id = d.donation_id
        JOIN resource_types rt ON d.resource_type_id = rt.resource_type_id
        JOIN relief_camps c ON da.camp_id = c.camp_id
        ORDER BY da.allocation_date DESC
        """
        return self.db.execute_query(query)
    
    def create_resource_for_camp(self, camp_id: int, resource_type_id: int, 
                               available: int, needed: int) -> Dict:
        """Create new resource entry for a camp"""
        try:
            query = """
            INSERT INTO resources (camp_id, resource_type_id, quantity_available, quantity_needed)
            VALUES (%s, %s, %s, %s)
            """
            params = (camp_id, resource_type_id, available, needed)
            
            success = self.db.execute_update(query, params)
            
            if success:
                return {"success": True, "message": "Resource created successfully"}
            else:
                return {"success": False, "message": "Failed to create resource"}
                
        except Exception as e:
            return {"success": False, "message": f"Error creating resource: {str(e)}"}
