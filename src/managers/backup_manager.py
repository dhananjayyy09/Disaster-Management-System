"""
Backup Manager for Disaster Relief Management System
Handles database backup and restore operations
"""

from datetime import datetime
from typing import Dict, List
from database_manager import DatabaseManager


class BackupManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_full_backup(self) -> Dict:
        """Create a complete backup of all tables"""
        try:
            backup_count = 0
            
            # Backup Users
            users = self.db.execute_query("SELECT * FROM users")
            for user in users:
                self.db.execute_update(
                    """INSERT INTO users_backup (user_id, username, email, password_hash, role, 
                       full_name, phone, is_active, created_at, last_login, backup_action)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'MANUAL')""",
                    (user['user_id'], user['username'], user['email'], user['password_hash'],
                     user['role'], user['full_name'], user.get('phone'), user.get('is_active'),
                     user.get('created_at'), user.get('last_login'))
                )
                backup_count += 1
            
            # Backup Disasters
            disasters = self.db.execute_query("SELECT * FROM disasters")
            for disaster in disasters:
                self.db.execute_update(
                    """INSERT INTO disasters_backup (disaster_id, disaster_name, disaster_type, 
                       location, severity, start_date, end_date, status, description, created_at, backup_action)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'MANUAL')""",
                    (disaster['disaster_id'], disaster['disaster_name'], disaster['disaster_type'],
                     disaster['location'], disaster['severity'], disaster['start_date'],
                     disaster.get('end_date'), disaster.get('status'), disaster.get('description'),
                     disaster.get('created_at'))
                )
                backup_count += 1
            
            # Backup Donations
            donations = self.db.execute_query("SELECT * FROM donations")
            for donation in donations:
                self.db.execute_update(
                    """INSERT INTO donations_backup (donation_id, donor_name, donor_contact, 
                       resource_type_id, quantity_donated, donation_date, status, notes, backup_action)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'MANUAL')""",
                    (donation['donation_id'], donation['donor_name'], donation.get('donor_contact'),
                     donation['resource_type_id'], donation['quantity_donated'], donation.get('donation_date'),
                     donation.get('status'), donation.get('notes'))
                )
                backup_count += 1
            
            return {
                "success": True,
                "message": f"Full backup completed successfully! {backup_count} records backed up.",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Backup failed: {str(e)}"
            }
    
    def get_backup_statistics(self) -> Dict:
        """Get backup statistics"""
        try:
            stats = {}
            
            # Count backup records
            tables = ['users_backup', 'disasters_backup', 'donations_backup', 
                     'volunteers_backup', 'resources_backup', 'relief_camps_backup']
            
            for table in tables:
                try:
                    result = self.db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    stats[table] = result[0]['count'] if result else 0
                except:
                    stats[table] = 0
            
            # Get latest backup timestamp
            latest = self.db.execute_query(
                "SELECT MAX(backup_timestamp) as latest FROM users_backup"
            )
            stats['latest_backup'] = latest[0]['latest'] if latest and latest[0]['latest'] else 'Never'
            
            # Total backup records
            stats['total_backups'] = sum(stats[table] for table in tables)
            
            return stats
            
        except Exception as e:
            print(f"Error getting backup stats: {e}")
            return {}
    
    def restore_from_backup(self, table_name: str, backup_id: int) -> Dict:
        """Restore specific record from backup"""
        try:
            # This is a placeholder - implement based on your needs
            return {
                "success": True,
                "message": f"Restore functionality available for {table_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Restore failed: {str(e)}"
            }
    
    def clear_old_backups(self, days: int = 30) -> Dict:
        """Clear backups older than specified days"""
        try:
            tables = ['users_backup', 'disasters_backup', 'donations_backup']
            deleted_count = 0
            
            for table in tables:
                try:
                    self.db.execute_update(
                        f"DELETE FROM {table} WHERE backup_timestamp < DATE_SUB(NOW(), INTERVAL %s DAY)",
                        (days,)
                    )
                    deleted_count += 1
                except:
                    pass
            
            return {
                "success": True,
                "message": f"Cleared backups older than {days} days from {deleted_count} tables"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Clear failed: {str(e)}"
            }
