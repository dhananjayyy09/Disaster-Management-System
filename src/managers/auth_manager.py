"""
Authentication Manager
Handles user authentication, registration, and session management
"""

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from typing import Dict, Optional, List
from database_manager import DatabaseManager


class AuthManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def register_user(self, username: str, email: str, password: str, 
                     role: str, full_name: str, phone: str = "") -> Dict:
        """Register a new user"""
        try:
            # Validate inputs
            if not username or not email or not password or not full_name:
                return {"success": False, "message": "All required fields must be filled"}
            
            if len(password) < 6:
                return {"success": False, "message": "Password must be at least 6 characters"}
            
            # Validate role
            valid_roles = ['admin', 'coordinator', 'volunteer']
            if role not in valid_roles:
                return {"success": False, "message": f"Invalid role. Must be one of: {', '.join(valid_roles)}"}
            
            # Check if username exists
            existing_user = self.db.execute_query(
                "SELECT user_id FROM users WHERE username = %s",
                (username,)
            )
            if existing_user:
                return {"success": False, "message": "Username already exists"}
            
            # Check if email exists
            existing_email = self.db.execute_query(
                "SELECT user_id FROM users WHERE email = %s",
                (email,)
            )
            if existing_email:
                return {"success": False, "message": "Email already registered"}
            
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Insert user
            query = """
            INSERT INTO users (username, email, password_hash, role, full_name, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            success = self.db.execute_update(query, (username, email, password_hash, role, full_name, phone))
            
            if success:
                return {"success": True, "message": f"User '{username}' registered successfully"}
            else:
                return {"success": False, "message": "Failed to register user"}
                
        except Exception as e:
            return {"success": False, "message": f"Error registering user: {str(e)}"}
    
    def login_user(self, username: str, password: str) -> Dict:
        """Authenticate user login"""
        try:
            if not username or not password:
                return {"success": False, "message": "Username and password are required"}
            
            # Get user from database
            query = """
            SELECT user_id, username, email, password_hash, role, full_name, is_active
            FROM users WHERE username = %s OR email = %s
            """
            users = self.db.execute_query(query, (username, username))
            
            if not users:
                return {"success": False, "message": "Invalid username or password"}
            
            user = users[0]
            
            # Check if user is active
            if not user.get('is_active', True):
                return {"success": False, "message": "Account is deactivated. Contact administrator."}
            
            # Verify password
            if not check_password_hash(user['password_hash'], password):
                return {"success": False, "message": "Invalid username or password"}
            
            # Update last login
            self.db.execute_update(
                "UPDATE users SET last_login = %s WHERE user_id = %s",
                (datetime.now(), user['user_id'])
            )
            
            # Remove password hash from response
            if 'password_hash' in user:
                del user['password_hash']
            
            return {
                "success": True,
                "message": "Login successful",
                "user": user
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error during login: {str(e)}"}
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user details by ID"""
        try:
            query = """
            SELECT user_id, username, email, role, full_name, phone, is_active, created_at, last_login
            FROM users WHERE user_id = %s
            """
            users = self.db.execute_query(query, (user_id,))
            return users[0] if users else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            query = """
            SELECT user_id, username, email, role, full_name, phone, is_active, created_at, last_login 
            FROM users 
            ORDER BY created_at DESC
            """
            return self.db.execute_query(query)
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_permissions(self, user_id: int) -> Dict:
        """Get user permissions based on role"""
        user = self.get_user_by_id(user_id)
        if not user:
            return {"can_view": False, "can_create": False, "can_edit": False, "can_delete": False}
        
        role = user.get('role', '')
        
        if role == 'admin':
            return {
                "can_view": True,
                "can_create": True,
                "can_edit": True,
                "can_delete": True,
                "can_manage_users": True,
                "can_view_reports": True
            }
        elif role == 'coordinator':
            return {
                "can_view": True,
                "can_create": True,
                "can_edit": True,
                "can_delete": False,
                "can_manage_users": False,
                "can_view_reports": True
            }
        elif role == 'volunteer':
            return {
                "can_view": True,
                "can_create": False,
                "can_edit": False,
                "can_delete": False,
                "can_manage_users": False,
                "can_view_reports": False
            }
        
        return {"can_view": False, "can_create": False, "can_edit": False, "can_delete": False}
    
    def update_user_profile(self, user_id: int, full_name: str, email: str, phone: str = "") -> Dict:
        """Update user profile"""
        try:
            query = "UPDATE users SET full_name = %s, email = %s, phone = %s WHERE user_id = %s"
            success = self.db.execute_update(query, (full_name, email, phone, user_id))
            
            if success:
                return {"success": True, "message": "Profile updated successfully"}
            else:
                return {"success": False, "message": "Failed to update profile"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict:
        """Change user password"""
        try:
            if len(new_password) < 6:
                return {"success": False, "message": "New password must be at least 6 characters"}
            
            # Get current user with password hash
            query = "SELECT password_hash FROM users WHERE user_id = %s"
            user_query = self.db.execute_query(query, (user_id,))
            
            if not user_query:
                return {"success": False, "message": "User not found"}
            
            # Verify current password
            if not check_password_hash(user_query[0]['password_hash'], current_password):
                return {"success": False, "message": "Current password is incorrect"}
            
            # Update password
            new_hash = generate_password_hash(new_password)
            success = self.db.execute_update(
                "UPDATE users SET password_hash = %s WHERE user_id = %s",
                (new_hash, user_id)
            )
            
            if success:
                return {"success": True, "message": "Password changed successfully"}
            else:
                return {"success": False, "message": "Failed to change password"}
                
        except Exception as e:
            return {"success": False, "message": f"Error changing password: {str(e)}"}
    
    def delete_user(self, user_id: int) -> Dict:
        """Delete user"""
        try:
            query = "DELETE FROM users WHERE user_id = %s"
            success = self.db.execute_update(query, (user_id,))
            
            if success:
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {"success": False, "message": "Failed to delete user"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def toggle_user_status(self, user_id: int) -> Dict:
        """Toggle user active status"""
        try:
            query = "UPDATE users SET is_active = NOT is_active WHERE user_id = %s"
            success = self.db.execute_update(query, (user_id,))
            
            if success:
                return {"success": True, "message": "User status updated"}
            else:
                return {"success": False, "message": "Failed to update status"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
