"""
Donation Management Module
Handles donation tracking, processing, and allocation
"""

from datetime import datetime
from typing import List, Dict, Optional
from database_manager import DatabaseManager

class DonationManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def record_donation(self, donor_name: str, donor_contact: str, resource_type_id: int,
                       quantity: int, notes: str = "") -> Dict:
        """Record a new donation"""
        try:
            # Validate inputs
            if not donor_name or not quantity or quantity <= 0:
                return {"success": False, "message": "Donor name and quantity are required"}
            
            # Check if resource type exists
            resource_types = self.db.get_resource_type_list()
            resource_type = next((rt for rt in resource_types if rt['resource_type_id'] == resource_type_id), None)
            
            if not resource_type:
                return {"success": False, "message": "Invalid resource type selected"}
            
            # Record donation
            success = self.db.add_donation(donor_name, donor_contact, resource_type_id, quantity, notes)
            
            if success:
                return {"success": True, "message": f"Donation of {quantity} {resource_type['unit']} {resource_type['type_name']} recorded successfully"}
            else:
                return {"success": False, "message": "Failed to record donation"}
                
        except Exception as e:
            return {"success": False, "message": f"Error recording donation: {str(e)}"}
    
    def get_donations_summary(self) -> List[Dict]:
        """Get summary of all donations with status"""
        donations = self.db.get_all_donations()
        
        for donation in donations:
            # Get allocation details
            allocations = self.db.execute_query(
                "SELECT da.*, c.camp_name FROM donation_allocations da "
                "JOIN relief_camps c ON da.camp_id = c.camp_id "
                "WHERE da.donation_id = %s",
                (donation['donation_id'],)
            )
            
            donation['allocations'] = allocations
            donation['allocated_quantity'] = sum(a['quantity_allocated'] for a in allocations)
            donation['remaining_quantity'] = donation['quantity_donated'] - donation['allocated_quantity']
            
            # Calculate days since donation
            donation_date = donation['donation_date']
            if isinstance(donation_date, str):
                donation_date = datetime.strptime(donation_date, '%Y-%m-%d %H:%M:%S')
            days_since = (datetime.now() - donation_date).days
            donation['days_since_donation'] = days_since
            
        return donations
    
    def get_pending_donations(self) -> List[Dict]:
        """Get donations that are pending allocation"""
        donations = self.get_donations_summary()
        return [d for d in donations if d['status'] == 'Pending' and d['remaining_quantity'] > 0]
    
    def get_donation_by_id(self, donation_id: int) -> Optional[Dict]:
        """Get specific donation details"""
        donations = self.get_donations_summary()
        return next((d for d in donations if d['donation_id'] == donation_id), None)
    
    def update_donation_status(self, donation_id: int, status: str) -> Dict:
        """Update donation status"""
        try:
            valid_statuses = ['Pending', 'Received', 'Allocated', 'Distributed']
            if status not in valid_statuses:
                return {"success": False, "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}
            
            success = self.db.execute_update(
                "UPDATE donations SET status = %s WHERE donation_id = %s",
                (status, donation_id)
            )
            
            if success:
                return {"success": True, "message": f"Donation status updated to '{status}'"}
            else:
                return {"success": False, "message": "Failed to update donation status"}
                
        except Exception as e:
            return {"success": False, "message": f"Error updating donation status: {str(e)}"}
    
    def get_donation_statistics(self) -> Dict:
        """Get donation statistics for dashboard"""
        donations = self.db.get_all_donations()
        
        stats = {
            'total_donations': len(donations),
            'pending_donations': len([d for d in donations if d['status'] == 'Pending']),
            'received_donations': len([d for d in donations if d['status'] == 'Received']),
            'allocated_donations': len([d for d in donations if d['status'] == 'Allocated']),
            'total_donated_quantity': sum(d['quantity_donated'] for d in donations),
            'donations_by_type': {},
            'recent_donations': [],
            'top_donors': {}
        }
        
        # Count donations by resource type
        for donation in donations:
            type_name = donation['type_name']
            if type_name not in stats['donations_by_type']:
                stats['donations_by_type'][type_name] = {'count': 0, 'quantity': 0}
            
            stats['donations_by_type'][type_name]['count'] += 1
            stats['donations_by_type'][type_name]['quantity'] += donation['quantity_donated']
        
        # Get recent donations (last 7 days)
        recent_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for donation in donations:
            donation_date = donation['donation_date']
            if isinstance(donation_date, str):
                donation_date = datetime.strptime(donation_date, '%Y-%m-%d %H:%M:%S')
            if (recent_date - donation_date).days <= 7:
                stats['recent_donations'].append(donation)
        
        # Get top donors
        donor_stats = {}
        for donation in donations:
            donor = donation['donor_name']
            if donor not in donor_stats:
                donor_stats[donor] = {'count': 0, 'total_quantity': 0}
            donor_stats[donor]['count'] += 1
            donor_stats[donor]['total_quantity'] += donation['quantity_donated']
        
        # Sort donors by total quantity
        stats['top_donors'] = dict(sorted(donor_stats.items(), 
                                        key=lambda x: x[1]['total_quantity'], 
                                        reverse=True)[:5])
        
        return stats
    
    def get_allocation_summary(self) -> List[Dict]:
        """Get summary of donation allocations"""
        return self.db.get_donation_allocation_summary()
    
    def get_donations_needing_allocation(self) -> List[Dict]:
        """Get donations that need allocation based on shortages"""
        pending_donations = self.get_pending_donations()
        allocations_needed = []
        
        for donation in pending_donations:
            resource_type_id = donation['resource_type_id']
            remaining_quantity = donation['remaining_quantity']
            
            # Find camps with shortages for this resource type
            shortages = self.db.execute_query(
                "SELECT r.*, rt.type_name, c.camp_name, d.disaster_name "
                "FROM resources r "
                "JOIN resource_types rt ON r.resource_type_id = rt.resource_type_id "
                "JOIN relief_camps c ON r.camp_id = c.camp_id "
                "JOIN disasters d ON c.disaster_id = d.disaster_id "
                "WHERE r.resource_type_id = %s AND r.quantity_needed > r.quantity_available",
                (resource_type_id,)
            )
            
            if shortages:
                total_shortage = sum(s['quantity_needed'] - s['quantity_available'] for s in shortages)
                donation['potential_impact'] = min(remaining_quantity, total_shortage)
                donation['affected_camps'] = len(shortages)
                allocations_needed.append(donation)
        
        # Sort by potential impact
        allocations_needed.sort(key=lambda x: x['potential_impact'], reverse=True)
        return allocations_needed
    
    def get_donation_trends(self) -> Dict:
        """Get donation trends over time"""
        # Get donations from last 30 days
        query = """
        SELECT DATE(donation_date) as donation_day, 
               COUNT(*) as donation_count,
               SUM(quantity_donated) as total_quantity
        FROM donations 
        WHERE donation_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        GROUP BY DATE(donation_date)
        ORDER BY donation_day
        """
        
        trends = self.db.execute_query(query)
        
        return {
            'daily_trends': trends,
            'total_days': len(trends),
            'average_daily_donations': len(trends) / 30 if trends else 0,
            'total_donations_period': sum(t['total_quantity'] for t in trends)
        }
