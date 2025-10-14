"""
Database Manager for Disaster Relief Management System
Handles all database operations and connections
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import List, Dict, Tuple, Optional

class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='DJdjdj12', database='disaster_relief_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"Successfully connected to MySQL database: {self.database}")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    def is_connected(self):
        """Check if database connection is active"""
        try:
            if self.connection and self.connection.is_connected():
                return True
            return False
        except:
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query and return results"""
        try:
            # Ensure connection is active
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            # Ensure connection is active
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing update: {e}")
            self.connection.rollback()
            return False
    
    # Disaster Management Methods
    def get_all_disasters(self) -> List[Dict]:
        """Get all disasters"""
        query = "SELECT * FROM disasters ORDER BY start_date DESC"
        return self.execute_query(query)
    
    def add_disaster(self, name: str, disaster_type: str, location: str, 
                    severity: str, start_date: str, description: str = "") -> bool:
        """Add new disaster"""
        query = """
        INSERT INTO disasters (disaster_name, disaster_type, location, severity, start_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, disaster_type, location, severity, start_date, description)
        return self.execute_update(query, params)
    
    def update_disaster_status(self, disaster_id: int, status: str) -> bool:
        """Update disaster status"""
        query = "UPDATE disasters SET status = %s WHERE disaster_id = %s"
        return self.execute_update(query, (status, disaster_id))
    
    # Relief Camp Management Methods
    def get_all_camps(self) -> List[Dict]:
        """Get all relief camps with disaster info"""
        query = """
        SELECT c.*, d.disaster_name, d.disaster_type 
        FROM relief_camps c
        JOIN disasters d ON c.disaster_id = d.disaster_id
        ORDER BY c.created_at DESC
        """
        return self.execute_query(query)
    
    def get_camps_by_disaster(self, disaster_id: int) -> List[Dict]:
        """Get camps for specific disaster"""
        query = """
        SELECT c.*, d.disaster_name 
        FROM relief_camps c
        JOIN disasters d ON c.disaster_id = d.disaster_id
        WHERE c.disaster_id = %s
        """
        return self.execute_query(query, (disaster_id,))
    
    def add_camp(self, name: str, disaster_id: int, location: str, 
                capacity: int, contact_person: str = "", contact_phone: str = "") -> bool:
        """Add new relief camp"""
        query = """
        INSERT INTO relief_camps (camp_name, disaster_id, location, capacity, contact_person, contact_phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, disaster_id, location, capacity, contact_person, contact_phone)
        return self.execute_update(query, params)
    
    def update_camp_occupancy(self, camp_id: int, occupancy: int) -> bool:
        """Update camp occupancy"""
        query = "UPDATE relief_camps SET current_occupancy = %s WHERE camp_id = %s"
        return self.execute_update(query, (occupancy, camp_id))
    
    # Resource Management Methods
    def get_camp_resources(self, camp_id: int) -> List[Dict]:
        """Get resources for specific camp"""
        query = """
        SELECT r.*, rt.type_name, rt.unit
        FROM resources r
        JOIN resource_types rt ON r.resource_type_id = rt.resource_type_id
        WHERE r.camp_id = %s
        ORDER BY rt.type_name
        """
        return self.execute_query(query, (camp_id,))
    
    def get_resource_shortages(self) -> List[Dict]:
        """Get resources with shortages (needed > available)"""
        query = """
        SELECT r.*, rt.type_name, rt.unit, c.camp_name, d.disaster_name
        FROM resources r
        JOIN resource_types rt ON r.resource_type_id = rt.resource_type_id
        JOIN relief_camps c ON r.camp_id = c.camp_id
        JOIN disasters d ON c.disaster_id = d.disaster_id
        WHERE r.quantity_needed > r.quantity_available
        ORDER BY (r.quantity_needed - r.quantity_available) DESC
        """
        return self.execute_query(query)
    
    def update_resource_quantity(self, resource_id: int, available: int, needed: int) -> bool:
        """Update resource quantities"""
        query = """
        UPDATE resources 
        SET quantity_available = %s, quantity_needed = %s 
        WHERE resource_id = %s
        """
        return self.execute_update(query, (available, needed, resource_id))
    
    # Volunteer Management Methods
    def get_all_volunteers(self) -> List[Dict]:
        """Get all volunteers"""
        query = "SELECT * FROM volunteers ORDER BY registration_date DESC"
        return self.execute_query(query)
    
    def get_available_volunteers(self) -> List[Dict]:
        """Get available volunteers"""
        query = "SELECT * FROM volunteers WHERE availability_status = 'Available'"
        return self.execute_query(query)
    
    def add_volunteer(self, first_name: str, last_name: str, email: str = "", 
                     phone: str = "", skills: str = "") -> bool:
        """Add new volunteer"""
        query = """
        INSERT INTO volunteers (first_name, last_name, email, phone, skills)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, email, phone, skills)
        return self.execute_update(query, params)
    
    def assign_volunteer(self, volunteer_id: int, camp_id: int, role: str, 
                        start_date: str) -> bool:
        """Assign volunteer to camp"""
        query = """
        INSERT INTO volunteer_assignments (volunteer_id, camp_id, role, start_date)
        VALUES (%s, %s, %s, %s)
        """
        params = (volunteer_id, camp_id, role, start_date)
        if self.execute_update(query, params):
            # Update volunteer status
            update_query = "UPDATE volunteers SET availability_status = 'Assigned' WHERE volunteer_id = %s"
            return self.execute_update(update_query, (volunteer_id,))
        return False
    
    # Donation Management Methods
    def get_all_donations(self) -> List[Dict]:
        """Get all donations"""
        query = """
        SELECT d.*, rt.type_name, rt.unit
        FROM donations d
        JOIN resource_types rt ON d.resource_type_id = rt.resource_type_id
        ORDER BY d.donation_date DESC
        """
        return self.execute_query(query)
    
    def add_donation(self, donor_name: str, donor_contact: str, resource_type_id: int,
                    quantity: int, notes: str = "") -> bool:
        """Add new donation"""
        query = """
        INSERT INTO donations (donor_name, donor_contact, resource_type_id, quantity_donated, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (donor_name, donor_contact, resource_type_id, quantity, notes)
        return self.execute_update(query, params)
    
    def allocate_donation(self, donation_id: int, camp_id: int, quantity: int) -> bool:
        """Allocate donation to camp"""
        query = """
        INSERT INTO donation_allocations (donation_id, camp_id, quantity_allocated)
        VALUES (%s, %s, %s)
        """
        return self.execute_update(query, (donation_id, camp_id, quantity))
    
    # Analytics and Reports
    def get_dashboard_summary(self) -> Dict:
        """Get summary data for dashboard"""
        summary = {}
        
        # Total disasters
        disasters = self.execute_query("SELECT COUNT(*) as count FROM disasters WHERE status = 'Active'")
        summary['active_disasters'] = disasters[0]['count'] if disasters else 0
        
        # Total camps
        camps = self.execute_query("SELECT COUNT(*) as count FROM relief_camps WHERE status = 'Active'")
        summary['active_camps'] = camps[0]['count'] if camps else 0
        
        # Total volunteers
        volunteers = self.execute_query("SELECT COUNT(*) as count FROM volunteers WHERE availability_status = 'Available'")
        summary['available_volunteers'] = volunteers[0]['count'] if volunteers else 0
        
        # Total occupancy
        occupancy = self.execute_query("SELECT SUM(current_occupancy) as total FROM relief_camps WHERE status = 'Active'")
        summary['total_occupancy'] = occupancy[0]['total'] if occupancy and occupancy[0]['total'] else 0
        
        # Critical shortages
        shortages = self.execute_query("SELECT COUNT(*) as count FROM resources WHERE quantity_needed > quantity_available")
        summary['critical_shortages'] = shortages[0]['count'] if shortages else 0
        
        return summary
    
    def get_resource_type_list(self) -> List[Dict]:
        """Get list of all resource types"""
        query = "SELECT * FROM resource_types ORDER BY type_name"
        return self.execute_query(query)
    
    def get_donation_allocation_summary(self) -> List[Dict]:
        """Get summary of donation allocations"""
        query = """
        SELECT da.*, d.donor_name, d.donation_date, rt.type_name, rt.unit, c.camp_name
        FROM donation_allocations da
        JOIN donations d ON da.donation_id = d.donation_id
        JOIN resource_types rt ON d.resource_type_id = rt.resource_type_id
        JOIN relief_camps c ON da.camp_id = c.camp_id
        ORDER BY da.allocation_date DESC
        """
        return self.execute_query(query)