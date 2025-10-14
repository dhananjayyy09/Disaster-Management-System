"""
Demo Version of Disaster Relief Management System
This version works without MySQL for demonstration purposes
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'demo-secret-key'

# Demo data - this simulates what would come from the database
DEMO_DATA = {
    'disasters': [
        {
            'disaster_id': 1,
            'disaster_name': 'Northern Earthquake 2024',
            'disaster_type': 'Earthquake',
            'location': 'Northern Region',
            'severity': 'High',
            'status': 'Active',
            'start_date': '2024-01-15',
            'days_active': 25,
            'camp_count': 2,
            'description': 'Major earthquake affecting northern districts'
        },
        {
            'disaster_id': 2,
            'disaster_name': 'Coastal Flooding',
            'disaster_type': 'Flood',
            'location': 'Coastal Areas',
            'severity': 'Medium',
            'status': 'Active',
            'start_date': '2024-02-01',
            'days_active': 10,
            'camp_count': 1,
            'description': 'Heavy rainfall causing widespread flooding'
        }
    ],
    'camps': [
        {
            'camp_id': 1,
            'camp_name': 'North Relief Center',
            'disaster_name': 'Northern Earthquake 2024',
            'disaster_type': 'Earthquake',
            'location': 'Northern District',
            'capacity': 500,
            'current_occupancy': 320,
            'occupancy_percentage': 64.0,
            'capacity_status': 'Moderate',
            'contact_person': 'John Smith',
            'contact_phone': '+1234567890',
            'status': 'Active'
        },
        {
            'camp_id': 2,
            'camp_name': 'Coastal Shelter',
            'disaster_name': 'Coastal Flooding',
            'disaster_type': 'Flood',
            'location': 'Coastal Town',
            'capacity': 300,
            'current_occupancy': 180,
            'occupancy_percentage': 60.0,
            'capacity_status': 'Moderate',
            'contact_person': 'Jane Doe',
            'contact_phone': '+1234567891',
            'status': 'Active'
        }
    ],
    'volunteers': [
        {
            'volunteer_id': 1,
            'first_name': 'Alice',
            'last_name': 'Williams',
            'email': 'alice@email.com',
            'phone': '+1234567893',
            'skills': 'Medical, First Aid',
            'availability_status': 'Available',
            'active_assignments': 0,
            'current_camps': [],
            'days_registered': 15
        },
        {
            'volunteer_id': 2,
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'email': 'charlie@email.com',
            'phone': '+1234567894',
            'skills': 'Logistics, Transportation',
            'availability_status': 'Assigned',
            'active_assignments': 1,
            'current_camps': ['North Relief Center'],
            'days_registered': 20
        }
    ],
    'donations': [
        {
            'donation_id': 1,
            'donor_name': 'Red Cross',
            'donor_contact': 'redcross@email.com',
            'type_name': 'Food',
            'unit': 'kg',
            'quantity_donated': 500,
            'status': 'Received',
            'donation_date': '2024-02-05 10:30:00',
            'days_since_donation': 5,
            'remaining_quantity': 300
        },
        {
            'donation_id': 2,
            'donor_name': 'Local Charity',
            'donor_contact': 'charity@email.com',
            'type_name': 'Water',
            'unit': 'liters',
            'quantity_donated': 1000,
            'status': 'Pending',
            'donation_date': '2024-02-08 14:20:00',
            'days_since_donation': 2,
            'remaining_quantity': 1000
        }
    ],
    'shortages': [
        {
            'camp_name': 'North Relief Center',
            'disaster_name': 'Northern Earthquake 2024',
            'type_name': 'Medical Supplies',
            'unit': 'units',
            'quantity_available': 50,
            'quantity_needed': 100,
            'resource_type_id': 4
        }
    ],
    'critical_shortages': [
        {
            'camp_name': 'North Relief Center',
            'disaster_name': 'Northern Earthquake 2024',
            'type_name': 'Medical Supplies',
            'unit': 'units',
            'quantity_available': 50,
            'quantity_needed': 150,
            'resource_type_id': 4,
            'shortage_severity': 'Critical'
        }
    ]
}

@app.route('/')
def index():
    """Home page - Dashboard"""
    summary = {
        'active_disasters': 2,
        'active_camps': 2,
        'available_volunteers': 1,
        'total_occupancy': 500,
        'critical_shortages': 1
    }
    
    disaster_stats = {
        'total_disasters': 2,
        'active_disasters': 2,
        'resolved_disasters': 0,
        'by_type': {'Earthquake': 1, 'Flood': 1},
        'by_severity': {'High': 1, 'Medium': 1}
    }
    
    camp_stats = {
        'total_camps': 2,
        'active_camps': 2,
        'total_capacity': 800,
        'total_occupancy': 500,
        'average_occupancy': 62.5,
        'overcrowded_camps': 0
    }
    
    volunteer_stats = {
        'total_volunteers': 2,
        'available_volunteers': 1,
        'assigned_volunteers': 1,
        'active_assignments': 1,
        'completed_assignments': 0
    }
    
    donation_stats = {
        'total_donations': 2,
        'pending_donations': 1,
        'received_donations': 1,
        'allocated_donations': 0,
        'total_donated_quantity': 1500
    }
    
    return render_template('dashboard.html',
                         summary=summary,
                         disaster_stats=disaster_stats,
                         camp_stats=camp_stats,
                         volunteer_stats=volunteer_stats,
                         donation_stats=donation_stats,
                         recent_disasters=DEMO_DATA['disasters'][:2],
                         recent_camps=DEMO_DATA['camps'][:2],
                         recent_donations=DEMO_DATA['donations'][:2])

@app.route('/disasters')
def disasters():
    """Disasters management page"""
    return render_template('disasters.html', disasters=DEMO_DATA['disasters'])

@app.route('/camps')
def camps():
    """Relief camps management page"""
    return render_template('camps.html', camps=DEMO_DATA['camps'])

@app.route('/resources')
def resources():
    """Resources management page"""
    return render_template('resources.html', 
                         shortages=DEMO_DATA['shortages'], 
                         critical_shortages=DEMO_DATA['critical_shortages'])

@app.route('/volunteers')
def volunteers():
    """Volunteers management page"""
    available_volunteers = [v for v in DEMO_DATA['volunteers'] if v['availability_status'] == 'Available']
    return render_template('volunteers.html', 
                         volunteers=DEMO_DATA['volunteers'],
                         available_volunteers=available_volunteers)

@app.route('/donations')
def donations():
    """Donations management page"""
    pending_donations = [d for d in DEMO_DATA['donations'] if d['status'] == 'Pending']
    return render_template('donations.html', 
                         donations=DEMO_DATA['donations'],
                         pending_donations=pending_donations)

@app.route('/reports')
def reports():
    """Reports and analytics page"""
    disaster_stats = {
        'total_disasters': 2,
        'active_disasters': 2,
        'resolved_disasters': 0,
        'by_type': {'Earthquake': 1, 'Flood': 1},
        'by_severity': {'High': 1, 'Medium': 1}
    }
    
    camp_stats = {
        'total_camps': 2,
        'active_camps': 2,
        'total_capacity': 800,
        'total_occupancy': 500,
        'average_occupancy': 62.5,
        'overcrowded_camps': 0
    }
    
    resource_stats = {
        'total_resource_types': 8,
        'total_shortages': 1,
        'critical_shortages': 1,
        'resources_by_type': {'Medical Supplies': 1},
        'top_shortages': DEMO_DATA['shortages']
    }
    
    volunteer_stats = {
        'total_volunteers': 2,
        'available_volunteers': 1,
        'assigned_volunteers': 1,
        'active_assignments': 1,
        'completed_assignments': 0,
        'volunteers_by_skill': {'Medical': 1, 'Logistics': 1}
    }
    
    donation_stats = {
        'total_donations': 2,
        'pending_donations': 1,
        'received_donations': 1,
        'allocated_donations': 0,
        'total_donated_quantity': 1500,
        'donations_by_type': {'Food': {'count': 1, 'quantity': 500}, 'Water': {'count': 1, 'quantity': 1000}},
        'recent_donations': DEMO_DATA['donations'],
        'top_donors': {'Red Cross': {'count': 1, 'total_quantity': 500}, 'Local Charity': {'count': 1, 'total_quantity': 1000}}
    }
    
    return render_template('reports.html',
                         disaster_stats=disaster_stats,
                         camp_stats=camp_stats,
                         resource_stats=resource_stats,
                         volunteer_stats=volunteer_stats,
                         donation_stats=donation_stats)

# API endpoints for charts
@app.route('/api/dashboard-stats')
def api_dashboard_stats():
    return jsonify({
        'active_disasters': 2,
        'active_camps': 2,
        'available_volunteers': 1,
        'total_occupancy': 500,
        'critical_shortages': 1
    })

@app.route('/api/charts/disaster-types')
def api_charts_disaster_types():
    return jsonify({'Earthquake': 1, 'Flood': 1})

@app.route('/api/charts/resource-shortages')
def api_charts_resource_shortages():
    return jsonify({'Medical Supplies': 1})

@app.route('/api/charts/volunteer-status')
def api_charts_volunteer_status():
    return jsonify({'Available': 1, 'Assigned': 1})

@app.route('/api/charts/donation-types')
def api_charts_donation_types():
    return jsonify({'Food': 500, 'Water': 1000})

# Form routes (demo versions)
@app.route('/disasters/add', methods=['GET', 'POST'])
def add_disaster():
    if request.method == 'POST':
        flash('Demo Mode: Disaster would be created successfully!', 'success')
        return redirect(url_for('disasters'))
    return render_template('add_disaster.html')

@app.route('/camps/add', methods=['GET', 'POST'])
def add_camp():
    if request.method == 'POST':
        flash('Demo Mode: Camp would be created successfully!', 'success')
        return redirect(url_for('camps'))
    return render_template('add_camp.html', disasters=DEMO_DATA['disasters'])

@app.route('/volunteers/add', methods=['GET', 'POST'])
def add_volunteer():
    if request.method == 'POST':
        flash('Demo Mode: Volunteer would be registered successfully!', 'success')
        return redirect(url_for('volunteers'))
    return render_template('add_volunteer.html')

@app.route('/donations/add', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        flash('Demo Mode: Donation would be recorded successfully!', 'success')
        return redirect(url_for('donations'))
    resource_types = [
        {'resource_type_id': 1, 'type_name': 'Food', 'unit': 'kg'},
        {'resource_type_id': 2, 'type_name': 'Water', 'unit': 'liters'},
        {'resource_type_id': 3, 'type_name': 'Blankets', 'unit': 'pieces'},
        {'resource_type_id': 4, 'type_name': 'Medical Supplies', 'unit': 'units'}
    ]
    return render_template('add_donation.html', resource_types=resource_types)

@app.route('/volunteers/assign', methods=['GET', 'POST'])
def assign_volunteer():
    if request.method == 'POST':
        flash('Demo Mode: Volunteer would be assigned successfully!', 'success')
        return redirect(url_for('volunteers'))
    available_volunteers = [v for v in DEMO_DATA['volunteers'] if v['availability_status'] == 'Available']
    return render_template('assign_volunteer.html', 
                         volunteers=available_volunteers, 
                         camps=DEMO_DATA['camps'])

@app.route('/donations/allocate', methods=['GET', 'POST'])
def allocate_donation():
    if request.method == 'POST':
        flash('Demo Mode: Donation would be allocated successfully!', 'success')
        return redirect(url_for('donations'))
    pending_donations = [d for d in DEMO_DATA['donations'] if d['status'] == 'Pending']
    return render_template('allocate_donation.html', 
                         pending_donations=pending_donations, 
                         camps=DEMO_DATA['camps'])

@app.route('/resources/auto-allocate', methods=['POST'])
def auto_allocate():
    flash('Demo Mode: Auto-allocation would be completed successfully!', 'success')
    return redirect(url_for('resources'))

if __name__ == '__main__':
    print("🌐 Starting Disaster Relief Management System - DEMO MODE")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("⚠️  Note: This is a demo version with sample data")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
