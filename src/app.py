"""
Disaster Relief Management System - Web Application
Flask-based web interface for managing disaster relief operations
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, Response
from functools import wraps
import json
from datetime import datetime, date, timedelta
import os
import sys
import csv
from io import StringIO

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_manager import DatabaseManager
from managers.disaster_manager import DisasterManager
from managers.camp_manager import CampManager
from managers.resource_manager import ResourceManager
from managers.volunteer_manager import VolunteerManager
from managers.donation_manager import DonationManager
from managers.auth_manager import AuthManager
from managers.backup_manager import BackupManager

# Configure paths for templates and static folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

print(f"📁 Template directory: {TEMPLATE_DIR}")
print(f"📁 Static directory: {STATIC_DIR}")

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production-12345')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize database and managers
db = DatabaseManager()
disaster_manager = DisasterManager(db)
camp_manager = CampManager(db)
resource_manager = ResourceManager(db)
volunteer_manager = VolunteerManager(db)
donation_manager = DonationManager(db)
auth_manager = AuthManager(db)
backup_manager = BackupManager(db)

def initialize_database():
    """Initialize database connection on first request"""
    if not db.connect():
        print("⚠️  Warning: Database connection failed")
        print("    Make sure MySQL is running and database is created")
        return False
    print("✅ Database connected successfully")
    return True

# Initialize database connection
initialize_database()

@app.before_request
def before_request():
    """Ensure database connection before each request"""
    if not db.is_connected():
        db.connect()

# ==================== AUTHENTICATION DECORATORS ====================

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to check if user has required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            
            user_role = session.get('role')
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
# ============ EXPORT ROUTES ============

@app.route('/export/disasters')
@login_required
def export_disasters():
    """Export disasters data as CSV"""
    try:
        disasters = db.get_all_disasters()
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Name', 'Type', 'Location', 'Severity', 'Start Date', 'End Date', 'Status', 'Description'])
        
        # Write data
        for d in disasters:
            writer.writerow([
                d.get('disaster_id', ''),
                d.get('disaster_name', ''),
                d.get('disaster_type', ''),
                d.get('location', ''),
                d.get('severity', ''),
                d.get('start_date', ''),
                d.get('end_date', ''),
                d.get('status', ''),
                d.get('description', '')
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=disasters.csv'}
        )
    except Exception as e:
        flash(f'Error exporting disasters: {str(e)}', 'error')
        return redirect(url_for('reports'))


@app.route('/export/camps')
@login_required
def export_camps():
    """Export camps data as CSV"""
    try:
        camps = db.get_all_camps()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Camp Name', 'Disaster', 'Location', 'Capacity', 'Current Occupancy', 'Status', 'Contact Person', 'Contact Phone'])
        
        # Write data
        for c in camps:
            writer.writerow([
                c.get('camp_id', ''),
                c.get('camp_name', ''),
                c.get('disaster_name', ''),
                c.get('location', ''),
                c.get('capacity', ''),
                c.get('current_occupancy', ''),
                c.get('status', ''),
                c.get('contact_person', ''),
                c.get('contact_phone', '')
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=camps.csv'}
        )
    except Exception as e:
        flash(f'Error exporting camps: {str(e)}', 'error')
        return redirect(url_for('reports'))


@app.route('/export/volunteers')
@login_required
def export_volunteers():
    """Export volunteers data as CSV"""
    try:
        volunteers = db.get_all_volunteers()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Skills', 'Status', 'Registration Date'])
        
        # Write data
        for v in volunteers:
            writer.writerow([
                v.get('volunteer_id', ''),
                v.get('first_name', ''),
                v.get('last_name', ''),
                v.get('email', ''),
                v.get('phone', ''),
                v.get('skills', ''),
                v.get('availability_status', ''),
                v.get('registration_date', '')
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=volunteers.csv'}
        )
    except Exception as e:
        flash(f'Error exporting volunteers: {str(e)}', 'error')
        return redirect(url_for('reports'))


@app.route('/export/donations')
@login_required
def export_donations():
    """Export donations data as CSV"""
    try:
        donations = db.get_all_donations()
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Donor Name', 'Contact', 'Resource Type', 'Quantity', 'Date', 'Status', 'Notes'])
        
        # Write data
        for d in donations:
            writer.writerow([
                d.get('donation_id', ''),
                d.get('donor_name', ''),
                d.get('donor_contact', ''),
                d.get('type_name', ''),
                d.get('quantity_donated', ''),
                d.get('donation_date', ''),
                d.get('status', ''),
                d.get('notes', '')
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=donations.csv'}
        )
    except Exception as e:
        flash(f'Error exporting donations: {str(e)}', 'error')
        return redirect(url_for('reports'))
    
    
# ==================== AUTHENTICATION ROUTES ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        result = auth_manager.login_user(username, password)
        
        if result['success']:
            user = result['user']
            session.permanent = True
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            
            flash(f"Welcome back, {user['full_name']}!", 'success')
            return redirect(url_for('index'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone', '')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
        else:
            result = auth_manager.register_user(username, email, password, role, full_name, phone)
            
            if result['success']:
                flash(result['message'] + ' Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash(result['message'], 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# ==================== MAIN APPLICATION ROUTES ====================

@app.route('/')
@login_required
def index():
    """Home page - Dashboard"""
    try:
        # Get dashboard summary
        summary = db.get_dashboard_summary()
        
        # Get user info
        user_role = session.get('role')
        user_name = session.get('full_name')
        
        # Get additional statistics
        disaster_stats = disaster_manager.get_disaster_statistics()
        camp_stats = camp_manager.get_camp_statistics()
        volunteer_stats = volunteer_manager.get_volunteer_statistics()
        donation_stats = donation_manager.get_donation_statistics()
        resource_stats = resource_manager.get_resource_statistics()
        
        # Get recent data for display
        recent_disasters = disaster_manager.get_disasters_summary()[:5]
        recent_camps = camp_manager.get_camps_summary()[:5]
        recent_donations = donation_manager.get_donations_summary()[:5]
        
        return render_template('dashboard.html',
                             summary=summary,
                             disaster_stats=disaster_stats,
                             camp_stats=camp_stats,
                             volunteer_stats=volunteer_stats,
                             donation_stats=donation_stats,
                             resource_stats=resource_stats,
                             recent_disasters=recent_disasters,
                             recent_camps=recent_camps,
                             recent_donations=recent_donations,
                             user_role=user_role,
                             user_name=user_name)
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", 'error')
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', summary={})

@app.route('/disasters')
@login_required
def disasters():
    """Disasters management page"""
    try:
        disasters_list = disaster_manager.get_disasters_summary()
        return render_template('disasters.html', disasters=disasters_list)
    except Exception as e:
        flash(f"Error loading disasters: {str(e)}", 'error')
        return render_template('disasters.html', disasters=[])

@app.route('/disasters/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def add_disaster():
    """Add new disaster - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            disaster_type = request.form['type']
            location = request.form['location']
            severity = request.form['severity']
            description = request.form.get('description', '')
            
            result = disaster_manager.create_disaster(name, disaster_type, location, severity, description)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error adding disaster: {str(e)}", 'error')
        
        return redirect(url_for('disasters'))
    
    return render_template('add_disaster.html')

@app.route('/camps')
@login_required
def camps():
    """Relief camps management page"""
    try:
        camps_list = camp_manager.get_camps_summary()
        return render_template('camps.html', camps=camps_list)
    except Exception as e:
        flash(f"Error loading camps: {str(e)}", 'error')
        return render_template('camps.html', camps=[])

@app.route('/camps/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def add_camp():
    """Add new relief camp - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            disaster_id = int(request.form['disaster_id'])
            location = request.form['location']
            capacity = int(request.form['capacity'])
            contact_person = request.form.get('contact_person', '')
            contact_phone = request.form.get('contact_phone', '')
            
            result = camp_manager.create_camp(name, disaster_id, location, capacity, contact_person, contact_phone)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error adding camp: {str(e)}", 'error')
        
        return redirect(url_for('camps'))
    
    # Get disasters for dropdown
    disasters_list = disaster_manager.get_disasters_summary()
    return render_template('add_camp.html', disasters=disasters_list)

@app.route('/resources')
@login_required
def resources():
    """Resources management page"""
    try:
        shortages = resource_manager.get_resource_shortages()
        critical_shortages = resource_manager.get_critical_shortages()
        return render_template('resources.html', 
                             shortages=shortages, 
                             critical_shortages=critical_shortages)
    except Exception as e:
        flash(f"Error loading resources: {str(e)}", 'error')
        return render_template('resources.html', shortages=[], critical_shortages=[])

@app.route('/resources/auto-allocate', methods=['POST'])
@login_required
@role_required('admin', 'coordinator')
def auto_allocate():
    """Auto-allocate donations to camps with shortages"""
    try:
        result = resource_manager.auto_allocate_donations()
        flash(result['message'], 'success' if result['success'] else 'error')
    except Exception as e:
        flash(f"Error in auto-allocation: {str(e)}", 'error')
    
    return redirect(url_for('resources'))

@app.route('/volunteers')
@login_required
def volunteers():
    """Volunteers management page"""
    try:
        volunteers_list = volunteer_manager.get_volunteers_summary()
        available_volunteers = volunteer_manager.get_available_volunteers_by_skill()
        return render_template('volunteers.html', 
                             volunteers=volunteers_list,
                             available_volunteers=available_volunteers)
    except Exception as e:
        flash(f"Error loading volunteers: {str(e)}", 'error')
        return render_template('volunteers.html', volunteers=[], available_volunteers=[])

@app.route('/volunteers/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def add_volunteer():
    """Add new volunteer - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form.get('email', '')
            phone = request.form.get('phone', '')
            skills = request.form.get('skills', '')
            
            result = volunteer_manager.register_volunteer(first_name, last_name, email, phone, skills)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error adding volunteer: {str(e)}", 'error')
        
        return redirect(url_for('volunteers'))
    
    return render_template('add_volunteer.html')

@app.route('/volunteers/assign', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def assign_volunteer():
    """Assign volunteer to camp - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            volunteer_id = int(request.form['volunteer_id'])
            camp_id = int(request.form['camp_id'])
            role = request.form['role']
            
            result = volunteer_manager.assign_volunteer_to_camp(volunteer_id, camp_id, role)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error assigning volunteer: {str(e)}", 'error')
        
        return redirect(url_for('volunteers'))
    
    # Get available volunteers and active camps
    volunteers_list = volunteer_manager.get_available_volunteers_by_skill()
    camps_list = camp_manager.get_camps_summary()
    return render_template('assign_volunteer.html', 
                         volunteers=volunteers_list, 
                         camps=camps_list)

@app.route('/donations')
@login_required
def donations():
    """Donations management page"""
    try:
        donations_list = donation_manager.get_donations_summary()
        pending_donations = donation_manager.get_pending_donations()
        return render_template('donations.html', 
                             donations=donations_list,
                             pending_donations=pending_donations)
    except Exception as e:
        flash(f"Error loading donations: {str(e)}", 'error')
        return render_template('donations.html', donations=[], pending_donations=[])

@app.route('/donations/add', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def add_donation():
    """Add new donation - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            donor_name = request.form['donor_name']
            donor_contact = request.form.get('donor_contact', '')
            resource_type_id = int(request.form['resource_type_id'])
            quantity = int(request.form['quantity'])
            notes = request.form.get('notes', '')
            
            result = donation_manager.record_donation(donor_name, donor_contact, resource_type_id, quantity, notes)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error adding donation: {str(e)}", 'error')
        
        return redirect(url_for('donations'))
    
    # Get resource types for dropdown
    resource_types = db.get_resource_type_list()
    return render_template('add_donation.html', resource_types=resource_types)

@app.route('/donations/allocate', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'coordinator')
def allocate_donation():
    """Allocate donation to camp - Admin and Coordinator only"""
    if request.method == 'POST':
        try:
            donation_id = int(request.form['donation_id'])
            camp_id = int(request.form['camp_id'])
            quantity = int(request.form['quantity'])
            
            result = resource_manager.allocate_donation_to_camp(donation_id, camp_id, quantity)
            
            if result['success']:
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error allocating donation: {str(e)}", 'error')
        
        return redirect(url_for('donations'))
    
    # GET request - show form
    try:
        # Get pending donations and active camps
        pending_donations = donation_manager.get_pending_donations()
        camps_list = camp_manager.get_camps_summary()
        
        # Dates are already formatted as strings by database_manager
        # No need to format again!
        
        return render_template('allocate_donation.html', 
                             pending_donations=pending_donations, 
                             camps=camps_list)
    except Exception as e:
        flash(f"Error loading allocation form: {str(e)}", 'error')
        print(f"Allocation form error: {e}")
        return redirect(url_for('donations'))
    

@app.route('/reports')
@login_required
def reports():
    """Reports and analytics page"""
    try:
        # Generate comprehensive report data
        disaster_stats = disaster_manager.get_disaster_statistics()
        camp_stats = camp_manager.get_camp_statistics()
        resource_stats = resource_manager.get_resource_statistics()
        volunteer_stats = volunteer_manager.get_volunteer_statistics()
        donation_stats = donation_manager.get_donation_statistics()
        
        return render_template('reports.html',
                             disaster_stats=disaster_stats,
                             camp_stats=camp_stats,
                             resource_stats=resource_stats,
                             volunteer_stats=volunteer_stats,
                             donation_stats=donation_stats)
    except Exception as e:
        flash(f"Error loading reports: {str(e)}", 'error')
        return render_template('reports.html')
    
    
# ==================== USER PROFILE ROUTES ====================

@app.route('/profile')
@login_required
def profile():
    """View user profile"""
    try:
        user_id = session.get('user_id')
        user = auth_manager.get_user_by_id(user_id)
        
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('index'))
        
        # Get user activity stats
        if user['role'] == 'volunteer':
            assignments = volunteer_manager.get_volunteer_assignments(user_id)
            user['activity_stats'] = {
                'total_assignments': len(assignments),
                'active_assignments': len([a for a in assignments if a.get('status') == 'Active'])
            }
        
        return render_template('profile.html', user=user)
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", 'error')
        return redirect(url_for('index'))


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            email = request.form.get('email')
            
            result = auth_manager.update_user_profile(user_id, full_name, email, phone)
            
            if result['success']:
                # Update session
                session['full_name'] = full_name
                flash(result['message'], 'success')
            else:
                flash(result['message'], 'error')
                
            return redirect(url_for('profile'))
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", 'error')
    
    user_id = session.get('user_id')
    user = auth_manager.get_user_by_id(user_id)
    return render_template('edit_profile.html', user=user)


@app.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('change_password'))
            
            result = auth_manager.change_password(user_id, current_password, new_password)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('profile'))
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error changing password: {str(e)}", 'error')
    
    return render_template('change_password.html')


# ==================== ADMIN ROUTES ====================

@app.route('/admin/users')
@login_required
@role_required('admin')
def manage_users():
    """Manage users - Admin only"""
    try:
        users = auth_manager.get_all_users()
        return render_template('manage_users.html', users=users)
    except Exception as e:
        flash(f"Error loading users: {str(e)}", 'error')
        return render_template('manage_users.html', users=[])


@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    """Add new user - Admin only"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone', '')
            
            result = auth_manager.register_user(username, email, password, role, full_name, phone)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('manage_users'))
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f"Error adding user: {str(e)}", 'error')
    
    return render_template('add_user.html')


@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete user - Admin only"""
    try:
        # Don't allow deleting yourself
        if user_id == session.get('user_id'):
            flash('Cannot delete your own account', 'error')
            return redirect(url_for('manage_users'))
        
        result = auth_manager.delete_user(user_id)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", 'error')
    
    return redirect(url_for('manage_users'))


@app.route('/admin/users/toggle-status/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    """Toggle user active status - Admin only"""
    try:
        result = auth_manager.toggle_user_status(user_id)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        flash(f"Error toggling user status: {str(e)}", 'error')
    
    return redirect(url_for('manage_users'))


@app.route('/admin/backup')
@login_required
@role_required('admin')
def backup_dashboard():
    """Backup dashboard - Admin only"""
    try:
        stats = backup_manager.get_backup_statistics()
        return render_template('backup_dashboard.html', stats=stats)
    except Exception as e:
        flash(f"Error loading backup dashboard: {str(e)}", 'error')
        return redirect(url_for('index'))


@app.route('/admin/backup/create', methods=['POST'])
@login_required
@role_required('admin')
def create_backup():
    """Create full backup - Admin only"""
    try:
        result = backup_manager.create_full_backup()
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        flash(f"Backup failed: {str(e)}", 'error')
    
    return redirect(url_for('backup_dashboard'))


@app.route('/admin/backup/clear', methods=['POST'])
@login_required
@role_required('admin')
def clear_backups():
    """Clear old backups - Admin only"""
    try:
        days = int(request.form.get('days', 30))
        result = backup_manager.clear_old_backups(days)
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
            
    except Exception as e:
        flash(f"Clear failed: {str(e)}", 'error')
    
    return redirect(url_for('backup_dashboard'))


@app.route('/settings')
@login_required
@role_required('admin', 'coordinator')
def settings():
    """System settings"""
    return render_template('settings.html') 

# ==================== API ENDPOINTS ====================

@app.route('/api/dashboard-stats')
@login_required
def api_dashboard_stats():
    """API endpoint for dashboard statistics"""
    try:
        summary = db.get_dashboard_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disasters')
@login_required
def api_disasters():
    """API endpoint for disasters data"""
    try:
        disasters_list = disaster_manager.get_disasters_summary()
        return jsonify(disasters_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/camps')
@login_required
def api_camps():
    """API endpoint for camps data"""
    try:
        camps_list = camp_manager.get_camps_summary()
        return jsonify(camps_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources')
@login_required
def api_resources():
    """API endpoint for resources data"""
    try:
        shortages = resource_manager.get_resource_shortages()
        return jsonify(shortages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volunteers')
@login_required
def api_volunteers():
    """API endpoint for volunteers data"""
    try:
        volunteers_list = volunteer_manager.get_volunteers_summary()
        return jsonify(volunteers_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/donations')
@login_required
def api_donations():
    """API endpoint for donations data"""
    try:
        donations_list = donation_manager.get_donations_summary()
        return jsonify(donations_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/disaster-types')
@login_required
def api_charts_disaster_types():
    """API endpoint for disaster types chart"""
    try:
        stats = disaster_manager.get_disaster_statistics()
        return jsonify(stats['by_type'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/resource-shortages')
@login_required
def api_charts_resource_shortages():
    """API endpoint for resource shortages chart"""
    try:
        stats = resource_manager.get_resource_statistics()
        return jsonify(stats['resources_by_type'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/volunteer-status')
@login_required
def api_charts_volunteer_status():
    """API endpoint for volunteer status chart"""
    try:
        stats = volunteer_manager.get_volunteer_statistics()
        return jsonify({
            'Available': stats['available_volunteers'],
            'Assigned': stats['assigned_volunteers']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/donation-types')
@login_required
def api_charts_donation_types():
    """API endpoint for donation types chart"""
    try:
        stats = donation_manager.get_donation_statistics()
        donation_data = {}
        for type_name, data in stats['donations_by_type'].items():
            donation_data[type_name] = data['quantity']
        return jsonify(donation_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🌐 Starting Disaster Relief Management System Web Application...")
    print("=" * 70)
    print(f"\n📱 Open your browser and go to: http://localhost:5000")
    print(f"📁 Templates folder: {TEMPLATE_DIR}")
    print(f"📁 Static folder: {STATIC_DIR}")
    print("\n✅ Login will be required for all pages")
    print("\n🔄 Press Ctrl+C to stop the server")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
