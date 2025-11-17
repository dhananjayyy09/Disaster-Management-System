"""
Volunteer Management Module
Handles volunteer registration, assignment, and scheduling
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from database_manager import DatabaseManager


class VolunteerManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        
    def register_volunteer(self, first_name: str, last_name: str, email: str = "", 
                          phone: str = "", skills: str = "") -> Dict:
        """Register a new volunteer"""
        try:
            # Validate inputs
            if not first_name or not last_name:
                return {"success": False, "message": "First name and last name are required"}
            
            # Check if email already exists (if provided)
            if email:
                existing_volunteers = self.db.get_all_volunteers()
                for volunteer in existing_volunteers:
                    if volunteer.get('email') == email:
                        return {"success": False, "message": "Email already registered"}
            
            # Register volunteer
            success = self.db.add_volunteer(first_name, last_name, email, phone, skills)
            
            if success:
                return {"success": True, "message": f"Volunteer {first_name} {last_name} registered successfully"}
            else:
                return {"success": False, "message": "Failed to register volunteer"}
                
        except Exception as e:
            return {"success": False, "message": f"Error registering volunteer: {str(e)}"}
    
    def get_volunteers_summary(self) -> List[Dict]:
        """Get summary of all volunteers with assignment info"""
        volunteers = self.db.get_all_volunteers()
        
        for volunteer in volunteers:
            # Get active assignments
            assignments = self.db.execute_query(
                "SELECT va.*, c.camp_name, d.disaster_name FROM volunteer_assignments va "
                "JOIN relief_camps c ON va.camp_id = c.camp_id "
                "JOIN disasters d ON c.disaster_id = d.disaster_id "
                "WHERE va.volunteer_id = %s AND va.status = 'Active'",
                (volunteer['volunteer_id'],)
            )
            
            volunteer['active_assignments'] = len(assignments)
            volunteer['current_camps'] = [a.get('camp_name', '') for a in assignments]
            
            # Calculate days since registration
            # registration_date is already a string from database_manager
            try:
                reg_date_str = volunteer.get('registration_date', '')
                if reg_date_str:
                    # Parse the string date
                    if ' ' in str(reg_date_str):
                        reg_date = datetime.strptime(str(reg_date_str), '%Y-%m-%d %H:%M:%S')
                    else:
                        reg_date = datetime.strptime(str(reg_date_str), '%Y-%m-%d')
                    
                    days_registered = (datetime.now() - reg_date).days
                    volunteer['days_registered'] = days_registered
                else:
                    volunteer['days_registered'] = 0
            except Exception as e:
                print(f"Error parsing volunteer registration date: {e}")
                volunteer['days_registered'] = 0
            
        return volunteers
    
    def assign_volunteer_to_camp(self, volunteer_id: int, camp_id: int, role: str, 
                               start_date: str = None) -> Dict:
        """Assign volunteer to a camp"""
        try:
            # Validate inputs
            if not volunteer_id or not camp_id or not role:
                return {"success": False, "message": "Volunteer, camp, and role are required"}
            
            # Check if volunteer is available
            volunteers = self.db.get_all_volunteers()
            volunteer = next((v for v in volunteers if v.get('volunteer_id') == volunteer_id), None)
            
            if not volunteer:
                return {"success": False, "message": "Volunteer not found"}
            
            if volunteer.get('availability_status') != 'Available':
                return {"success": False, "message": "Volunteer is not available for assignment"}
            
            # Check if camp exists
            camps = self.db.get_all_camps()
            camp = next((c for c in camps if c.get('camp_id') == camp_id), None)
            
            if not camp:
                return {"success": False, "message": "Camp not found"}
            
            # Set start date to today if not provided
            if not start_date:
                start_date = date.today().strftime('%Y-%m-%d')
            
            # Assign volunteer
            success = self.db.assign_volunteer(volunteer_id, camp_id, role, start_date)
            
            if success:
                return {"success": True, "message": f"Volunteer assigned to {camp.get('camp_name', 'camp')} as {role}"}
            else:
                return {"success": False, "message": "Failed to assign volunteer"}
                
        except Exception as e:
            return {"success": False, "message": f"Error assigning volunteer: {str(e)}"}
    
    def get_available_volunteers_by_skill(self, skill_keyword: str = "") -> List[Dict]:
        """Get available volunteers filtered by skill"""
        volunteers = self.db.get_available_volunteers()
        
        if skill_keyword:
            filtered = []
            for volunteer in volunteers:
                skills = volunteer.get('skills', '').lower()
                if skill_keyword.lower() in skills:
                    filtered.append(volunteer)
            return filtered
        
        return volunteers
    
    def get_volunteer_assignments(self, volunteer_id: int = None) -> List[Dict]:
        """Get volunteer assignments (all or for specific volunteer)"""
        try:
            if volunteer_id:
                query = """
                SELECT va.*, v.first_name, v.last_name, c.camp_name, d.disaster_name
                FROM volunteer_assignments va
                JOIN volunteers v ON va.volunteer_id = v.volunteer_id
                JOIN relief_camps c ON va.camp_id = c.camp_id
                JOIN disasters d ON c.disaster_id = d.disaster_id
                WHERE va.volunteer_id = %s
                ORDER BY va.start_date DESC
                """
                return self.db.execute_query(query, (volunteer_id,))
            else:
                query = """
                SELECT va.*, v.first_name, v.last_name, c.camp_name, d.disaster_name
                FROM volunteer_assignments va
                JOIN volunteers v ON va.volunteer_id = v.volunteer_id
                JOIN relief_camps c ON va.camp_id = c.camp_id
                JOIN disasters d ON c.disaster_id = d.disaster_id
                ORDER BY va.start_date DESC
                """
                return self.db.execute_query(query)
        except Exception as e:
            print(f"Error getting volunteer assignments: {e}")
            return []
    
    def complete_assignment(self, assignment_id: int) -> Dict:
        """Mark volunteer assignment as completed"""
        try:
            # Update assignment status
            query = "UPDATE volunteer_assignments SET status = 'Completed', end_date = %s WHERE assignment_id = %s"
            end_date = date.today().strftime('%Y-%m-%d')
            success = self.db.execute_update(query, (end_date, assignment_id))
            
            if success:
                # Get volunteer ID and update availability
                assignment = self.db.execute_query(
                    "SELECT volunteer_id FROM volunteer_assignments WHERE assignment_id = %s",
                    (assignment_id,)
                )
                
                if assignment:
                    volunteer_id = assignment[0].get('volunteer_id')
                    # Check if volunteer has other active assignments
                    active_assignments = self.db.execute_query(
                        "SELECT COUNT(*) as count FROM volunteer_assignments "
                        "WHERE volunteer_id = %s AND status = 'Active'",
                        (volunteer_id,)
                    )
                    
                    # If no other active assignments, make volunteer available
                    if active_assignments and active_assignments[0].get('count', 0) == 0:
                        self.db.execute_update(
                            "UPDATE volunteers SET availability_status = 'Available' WHERE volunteer_id = %s",
                            (volunteer_id,)
                        )
                
                return {"success": True, "message": "Assignment marked as completed"}
            else:
                return {"success": False, "message": "Failed to complete assignment"}
                
        except Exception as e:
            return {"success": False, "message": f"Error completing assignment: {str(e)}"}
    
    def get_volunteer_statistics(self) -> Dict:
        """Get volunteer statistics for dashboard"""
        volunteers = self.db.get_all_volunteers()
        assignments = self.get_volunteer_assignments()
        
        stats = {
            'total_volunteers': len(volunteers),
            'available_volunteers': len([v for v in volunteers if v.get('availability_status') == 'Available']),
            'assigned_volunteers': len([v for v in volunteers if v.get('availability_status') == 'Assigned']),
            'active_assignments': len([a for a in assignments if a.get('status') == 'Active']),
            'completed_assignments': len([a for a in assignments if a.get('status') == 'Completed']),
            'volunteers_by_skill': {}
        }
        
        # Count volunteers by skill
        for volunteer in volunteers:
            skills = volunteer.get('skills', '').split(',')
            for skill in skills:
                skill = skill.strip()
                if skill:
                    stats['volunteers_by_skill'][skill] = stats['volunteers_by_skill'].get(skill, 0) + 1
        
        return stats
    
    def get_volunteer_performance_report(self) -> List[Dict]:
        """Get volunteer performance report"""
        try:
            query = """
            SELECT v.volunteer_id, v.first_name, v.last_name, v.skills,
                   COUNT(va.assignment_id) as total_assignments,
                   COUNT(CASE WHEN va.status = 'Completed' THEN 1 END) as completed_assignments,
                   COUNT(CASE WHEN va.status = 'Active' THEN 1 END) as active_assignments,
                   v.registration_date
            FROM volunteers v
            LEFT JOIN volunteer_assignments va ON v.volunteer_id = va.volunteer_id
            GROUP BY v.volunteer_id, v.first_name, v.last_name, v.skills, v.registration_date
            ORDER BY total_assignments DESC
            """
            return self.db.execute_query(query)
        except Exception as e:
            print(f"Error getting volunteer performance report: {e}")
            return []
