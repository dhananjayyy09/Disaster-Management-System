"""
Disaster Relief Management System - Main Application
Tkinter-based GUI for managing disasters, camps, resources, volunteers, and donations
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, date

from database_manager import DatabaseManager
from disaster_manager import DisasterManager
from camp_manager import CampManager
from resource_manager import ResourceManager
from volunteer_manager import VolunteerManager
from donation_manager import DonationManager

class DisasterReliefApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disaster Relief Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database and managers
        self.db = DatabaseManager()
        if not self.db.connect():
            messagebox.showerror("Database Error", "Failed to connect to database. Please check your MySQL connection.")
            return
            
        self.disaster_manager = DisasterManager(self.db)
        self.camp_manager = CampManager(self.db)
        self.resource_manager = ResourceManager(self.db)
        self.volunteer_manager = VolunteerManager(self.db)
        self.donation_manager = DonationManager(self.db)
        
        # Create main interface
        self.create_main_interface()
        
        # Load initial data
        self.refresh_dashboard()
    
    def create_main_interface(self):
        """Create the main interface with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_disasters_tab()
        self.create_camps_tab()
        self.create_resources_tab()
        self.create_volunteers_tab()
        self.create_donations_tab()
        self.create_reports_tab()
    
    def create_dashboard_tab(self):
        """Create dashboard tab with overview"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Dashboard title
        title_label = tk.Label(dashboard_frame, text="Disaster Relief Management Dashboard", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Create summary cards
        self.create_summary_cards(dashboard_frame)
        
        # Create charts frame
        charts_frame = tk.Frame(dashboard_frame, bg='#f0f0f0')
        charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create charts
        self.create_dashboard_charts(charts_frame)
        
        # Refresh button
        refresh_btn = tk.Button(dashboard_frame, text="Refresh Dashboard", 
                               command=self.refresh_dashboard, bg='#4CAF50', fg='white')
        refresh_btn.pack(pady=10)
    
    def create_summary_cards(self, parent):
        """Create summary cards for dashboard"""
        cards_frame = tk.Frame(parent, bg='#f0f0f0')
        cards_frame.pack(fill='x', padx=10, pady=10)
        
        # Get summary data
        summary = self.db.get_dashboard_summary()
        
        # Create cards
        card_configs = [
            ("Active Disasters", summary['active_disasters'], '#FF6B6B'),
            ("Active Camps", summary['active_camps'], '#4ECDC4'),
            ("Available Volunteers", summary['available_volunteers'], '#45B7D1'),
            ("Total Occupancy", summary['total_occupancy'], '#96CEB4'),
            ("Critical Shortages", summary['critical_shortages'], '#FECA57')
        ]
        
        self.summary_cards = {}
        for i, (title, value, color) in enumerate(card_configs):
            card = tk.Frame(cards_frame, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            
            title_label = tk.Label(card, text=title, font=('Arial', 10, 'bold'), 
                                  bg=color, fg='white')
            title_label.pack(pady=(10, 5))
            
            value_label = tk.Label(card, text=str(value), font=('Arial', 20, 'bold'), 
                                  bg=color, fg='white')
            value_label.pack(pady=(0, 10))
            
            self.summary_cards[title] = value_label
        
        # Configure grid weights
        for i in range(len(card_configs)):
            cards_frame.grid_columnconfigure(i, weight=1)
    
    def create_dashboard_charts(self, parent):
        """Create charts for dashboard"""
        # Create figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Disaster Relief Analytics', fontsize=16)
        
        # Chart 1: Disaster Types
        disaster_stats = self.disaster_manager.get_disaster_statistics()
        if disaster_stats['by_type']:
            ax1.pie(disaster_stats['by_type'].values(), labels=disaster_stats['by_type'].keys(), autopct='%1.1f%%')
            ax1.set_title('Disasters by Type')
        
        # Chart 2: Resource Shortages
        resource_stats = self.resource_manager.get_resource_statistics()
        if resource_stats['resources_by_type']:
            ax2.bar(resource_stats['resources_by_type'].keys(), resource_stats['resources_by_type'].values())
            ax2.set_title('Resource Shortages by Type')
            ax2.tick_params(axis='x', rotation=45)
        
        # Chart 3: Volunteer Status
        volunteer_stats = self.volunteer_manager.get_volunteer_statistics()
        status_data = {
            'Available': volunteer_stats['available_volunteers'],
            'Assigned': volunteer_stats['assigned_volunteers']
        }
        ax3.bar(status_data.keys(), status_data.values())
        ax3.set_title('Volunteer Status')
        
        # Chart 4: Donation Trends
        donation_stats = self.donation_manager.get_donation_statistics()
        if donation_stats['donations_by_type']:
            types = list(donation_stats['donations_by_type'].keys())
            quantities = [donation_stats['donations_by_type'][t]['quantity'] for t in types]
            ax4.bar(types, quantities)
            ax4.set_title('Donations by Type')
            ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_disasters_tab(self):
        """Create disasters management tab"""
        disasters_frame = ttk.Frame(self.notebook)
        self.notebook.add(disasters_frame, text="Disasters")
        
        # Title
        title_label = tk.Label(disasters_frame, text="Disaster Management", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(disasters_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        add_disaster_btn = tk.Button(buttons_frame, text="Add Disaster", 
                                    command=self.add_disaster_dialog, bg='#4CAF50', fg='white')
        add_disaster_btn.pack(side='left', padx=5)
        
        refresh_disasters_btn = tk.Button(buttons_frame, text="Refresh", 
                                         command=self.refresh_disasters, bg='#2196F3', fg='white')
        refresh_disasters_btn.pack(side='left', padx=5)
        
        # Treeview for disasters
        columns = ('ID', 'Name', 'Type', 'Location', 'Severity', 'Status', 'Start Date', 'Camps')
        self.disasters_tree = ttk.Treeview(disasters_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.disasters_tree.heading(col, text=col)
            self.disasters_tree.column(col, width=100)
        
        self.disasters_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar_disasters = ttk.Scrollbar(disasters_frame, orient='vertical', command=self.disasters_tree.yview)
        self.disasters_tree.configure(yscrollcommand=scrollbar_disasters.set)
        
        # Load disasters data
        self.refresh_disasters()
    
    def create_camps_tab(self):
        """Create camps management tab"""
        camps_frame = ttk.Frame(self.notebook)
        self.notebook.add(camps_frame, text="Relief Camps")
        
        # Title
        title_label = tk.Label(camps_frame, text="Relief Camp Management", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(camps_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        add_camp_btn = tk.Button(buttons_frame, text="Add Camp", 
                                command=self.add_camp_dialog, bg='#4CAF50', fg='white')
        add_camp_btn.pack(side='left', padx=5)
        
        refresh_camps_btn = tk.Button(buttons_frame, text="Refresh", 
                                     command=self.refresh_camps, bg='#2196F3', fg='white')
        refresh_camps_btn.pack(side='left', padx=5)
        
        # Treeview for camps
        columns = ('ID', 'Name', 'Disaster', 'Location', 'Capacity', 'Occupancy', '%', 'Status')
        self.camps_tree = ttk.Treeview(camps_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.camps_tree.heading(col, text=col)
            self.camps_tree.column(col, width=100)
        
        self.camps_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load camps data
        self.refresh_camps()
    
    def create_resources_tab(self):
        """Create resources management tab"""
        resources_frame = ttk.Frame(self.notebook)
        self.notebook.add(resources_frame, text="Resources")
        
        # Title
        title_label = tk.Label(resources_frame, text="Resource Management", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(resources_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        view_shortages_btn = tk.Button(buttons_frame, text="View Shortages", 
                                      command=self.show_resource_shortages, bg='#FF5722', fg='white')
        view_shortages_btn.pack(side='left', padx=5)
        
        auto_allocate_btn = tk.Button(buttons_frame, text="Auto Allocate", 
                                     command=self.auto_allocate_donations, bg='#4CAF50', fg='white')
        auto_allocate_btn.pack(side='left', padx=5)
        
        refresh_resources_btn = tk.Button(buttons_frame, text="Refresh", 
                                         command=self.refresh_resources, bg='#2196F3', fg='white')
        refresh_resources_btn.pack(side='left', padx=5)
        
        # Treeview for resources
        columns = ('Camp', 'Resource', 'Available', 'Needed', 'Shortage', 'Status')
        self.resources_tree = ttk.Treeview(resources_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.resources_tree.heading(col, text=col)
            self.resources_tree.column(col, width=120)
        
        self.resources_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load resources data
        self.refresh_resources()
    
    def create_volunteers_tab(self):
        """Create volunteers management tab"""
        volunteers_frame = ttk.Frame(self.notebook)
        self.notebook.add(volunteers_frame, text="Volunteers")
        
        # Title
        title_label = tk.Label(volunteers_frame, text="Volunteer Management", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(volunteers_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        add_volunteer_btn = tk.Button(buttons_frame, text="Add Volunteer", 
                                     command=self.add_volunteer_dialog, bg='#4CAF50', fg='white')
        add_volunteer_btn.pack(side='left', padx=5)
        
        assign_volunteer_btn = tk.Button(buttons_frame, text="Assign Volunteer", 
                                        command=self.assign_volunteer_dialog, bg='#FF9800', fg='white')
        assign_volunteer_btn.pack(side='left', padx=5)
        
        refresh_volunteers_btn = tk.Button(buttons_frame, text="Refresh", 
                                          command=self.refresh_volunteers, bg='#2196F3', fg='white')
        refresh_volunteers_btn.pack(side='left', padx=5)
        
        # Treeview for volunteers
        columns = ('ID', 'Name', 'Email', 'Phone', 'Skills', 'Status', 'Assignments')
        self.volunteers_tree = ttk.Treeview(volunteers_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.volunteers_tree.heading(col, text=col)
            self.volunteers_tree.column(col, width=120)
        
        self.volunteers_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load volunteers data
        self.refresh_volunteers()
    
    def create_donations_tab(self):
        """Create donations management tab"""
        donations_frame = ttk.Frame(self.notebook)
        self.notebook.add(donations_frame, text="Donations")
        
        # Title
        title_label = tk.Label(donations_frame, text="Donation Management", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(donations_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        add_donation_btn = tk.Button(buttons_frame, text="Add Donation", 
                                    command=self.add_donation_dialog, bg='#4CAF50', fg='white')
        add_donation_btn.pack(side='left', padx=5)
        
        allocate_donation_btn = tk.Button(buttons_frame, text="Allocate Donation", 
                                         command=self.allocate_donation_dialog, bg='#FF9800', fg='white')
        allocate_donation_btn.pack(side='left', padx=5)
        
        refresh_donations_btn = tk.Button(buttons_frame, text="Refresh", 
                                         command=self.refresh_donations, bg='#2196F3', fg='white')
        refresh_donations_btn.pack(side='left', padx=5)
        
        # Treeview for donations
        columns = ('ID', 'Donor', 'Resource', 'Quantity', 'Status', 'Date', 'Remaining')
        self.donations_tree = ttk.Treeview(donations_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.donations_tree.heading(col, text=col)
            self.donations_tree.column(col, width=120)
        
        self.donations_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load donations data
        self.refresh_donations()
    
    def create_reports_tab(self):
        """Create reports and analytics tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Title
        title_label = tk.Label(reports_frame, text="Reports & Analytics", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(reports_frame, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        generate_report_btn = tk.Button(buttons_frame, text="Generate Report", 
                                       command=self.generate_comprehensive_report, bg='#4CAF50', fg='white')
        generate_report_btn.pack(side='left', padx=5)
        
        export_data_btn = tk.Button(buttons_frame, text="Export Data", 
                                   command=self.export_data, bg='#2196F3', fg='white')
        export_data_btn.pack(side='left', padx=5)
        
        # Text widget for reports
        self.reports_text = tk.Text(reports_frame, height=20, width=80)
        self.reports_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for reports
        scrollbar_reports = ttk.Scrollbar(reports_frame, orient='vertical', command=self.reports_text.yview)
        self.reports_text.configure(yscrollcommand=scrollbar_reports.set)
    
    # Dialog methods
    def add_disaster_dialog(self):
        """Dialog to add new disaster"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Disaster")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Disaster Name:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Disaster Type:").pack(pady=5)
        type_var = tk.StringVar(value="Earthquake")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=['Earthquake', 'Flood', 'Wildfire', 'Hurricane', 'Tornado', 'Other'])
        type_combo.pack(pady=5)
        
        tk.Label(dialog, text="Location:").pack(pady=5)
        location_entry = tk.Entry(dialog, width=40)
        location_entry.pack(pady=5)
        
        tk.Label(dialog, text="Severity:").pack(pady=5)
        severity_var = tk.StringVar(value="Medium")
        severity_combo = ttk.Combobox(dialog, textvariable=severity_var, 
                                     values=['Low', 'Medium', 'High', 'Critical'])
        severity_combo.pack(pady=5)
        
        tk.Label(dialog, text="Description:").pack(pady=5)
        description_text = tk.Text(dialog, height=3, width=40)
        description_text.pack(pady=5)
        
        def save_disaster():
            name = name_entry.get()
            disaster_type = type_var.get()
            location = location_entry.get()
            severity = severity_var.get()
            description = description_text.get("1.0", tk.END).strip()
            
            result = self.disaster_manager.create_disaster(name, disaster_type, location, severity, description)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_disasters()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Save", command=save_disaster, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    def add_camp_dialog(self):
        """Dialog to add new relief camp"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Relief Camp")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get disasters for dropdown
        disasters = self.disaster_manager.get_disasters_summary()
        
        # Form fields
        tk.Label(dialog, text="Camp Name:").pack(pady=5)
        name_entry = tk.Entry(dialog, width=40)
        name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Disaster:").pack(pady=5)
        disaster_var = tk.StringVar()
        disaster_combo = ttk.Combobox(dialog, textvariable=disaster_var, 
                                     values=[f"{d['disaster_name']} (ID: {d['disaster_id']})" for d in disasters])
        disaster_combo.pack(pady=5)
        
        tk.Label(dialog, text="Location:").pack(pady=5)
        location_entry = tk.Entry(dialog, width=40)
        location_entry.pack(pady=5)
        
        tk.Label(dialog, text="Capacity:").pack(pady=5)
        capacity_entry = tk.Entry(dialog, width=40)
        capacity_entry.pack(pady=5)
        
        tk.Label(dialog, text="Contact Person:").pack(pady=5)
        contact_entry = tk.Entry(dialog, width=40)
        contact_entry.pack(pady=5)
        
        tk.Label(dialog, text="Contact Phone:").pack(pady=5)
        phone_entry = tk.Entry(dialog, width=40)
        phone_entry.pack(pady=5)
        
        def save_camp():
            name = name_entry.get()
            disaster_text = disaster_var.get()
            location = location_entry.get()
            capacity = capacity_entry.get()
            contact = contact_entry.get()
            phone = phone_entry.get()
            
            # Extract disaster ID
            try:
                disaster_id = int(disaster_text.split("ID: ")[1].split(")")[0])
                capacity = int(capacity)
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Please select a valid disaster and enter a valid capacity")
                return
            
            result = self.camp_manager.create_camp(name, disaster_id, location, capacity, contact, phone)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_camps()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Save", command=save_camp, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    def add_volunteer_dialog(self):
        """Dialog to add new volunteer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Volunteer")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="First Name:").pack(pady=5)
        first_name_entry = tk.Entry(dialog, width=40)
        first_name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Last Name:").pack(pady=5)
        last_name_entry = tk.Entry(dialog, width=40)
        last_name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = tk.Entry(dialog, width=40)
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(dialog, width=40)
        phone_entry.pack(pady=5)
        
        tk.Label(dialog, text="Skills:").pack(pady=5)
        skills_text = tk.Text(dialog, height=3, width=40)
        skills_text.pack(pady=5)
        
        def save_volunteer():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            skills = skills_text.get("1.0", tk.END).strip()
            
            result = self.volunteer_manager.register_volunteer(first_name, last_name, email, phone, skills)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_volunteers()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Save", command=save_volunteer, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    def add_donation_dialog(self):
        """Dialog to add new donation"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Donation")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get resource types
        resource_types = self.db.get_resource_type_list()
        
        # Form fields
        tk.Label(dialog, text="Donor Name:").pack(pady=5)
        donor_entry = tk.Entry(dialog, width=40)
        donor_entry.pack(pady=5)
        
        tk.Label(dialog, text="Donor Contact:").pack(pady=5)
        contact_entry = tk.Entry(dialog, width=40)
        contact_entry.pack(pady=5)
        
        tk.Label(dialog, text="Resource Type:").pack(pady=5)
        resource_var = tk.StringVar()
        resource_combo = ttk.Combobox(dialog, textvariable=resource_var, 
                                     values=[f"{rt['type_name']} ({rt['unit']})" for rt in resource_types])
        resource_combo.pack(pady=5)
        
        tk.Label(dialog, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(dialog, width=40)
        quantity_entry.pack(pady=5)
        
        tk.Label(dialog, text="Notes:").pack(pady=5)
        notes_text = tk.Text(dialog, height=3, width=40)
        notes_text.pack(pady=5)
        
        def save_donation():
            donor_name = donor_entry.get()
            donor_contact = contact_entry.get()
            resource_text = resource_var.get()
            quantity = quantity_entry.get()
            notes = notes_text.get("1.0", tk.END).strip()
            
            # Extract resource type ID
            try:
                resource_type_id = next(rt['resource_type_id'] for rt in resource_types 
                                       if rt['type_name'] in resource_text)
                quantity = int(quantity)
            except (ValueError, StopIteration):
                messagebox.showerror("Error", "Please select a valid resource type and enter a valid quantity")
                return
            
            result = self.donation_manager.record_donation(donor_name, donor_contact, resource_type_id, quantity, notes)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_donations()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Save", command=save_donation, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    def assign_volunteer_dialog(self):
        """Dialog to assign volunteer to camp"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Volunteer")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get available volunteers and active camps
        volunteers = self.volunteer_manager.get_available_volunteers_by_skill()
        camps = self.camp_manager.get_camps_summary()
        
        # Form fields
        tk.Label(dialog, text="Volunteer:").pack(pady=5)
        volunteer_var = tk.StringVar()
        volunteer_combo = ttk.Combobox(dialog, textvariable=volunteer_var, 
                                      values=[f"{v['first_name']} {v['last_name']} (ID: {v['volunteer_id']})" for v in volunteers])
        volunteer_combo.pack(pady=5)
        
        tk.Label(dialog, text="Camp:").pack(pady=5)
        camp_var = tk.StringVar()
        camp_combo = ttk.Combobox(dialog, textvariable=camp_var, 
                                 values=[f"{c['camp_name']} (ID: {c['camp_id']})" for c in camps])
        camp_combo.pack(pady=5)
        
        tk.Label(dialog, text="Role:").pack(pady=5)
        role_entry = tk.Entry(dialog, width=40)
        role_entry.pack(pady=5)
        
        def save_assignment():
            volunteer_text = volunteer_var.get()
            camp_text = camp_var.get()
            role = role_entry.get()
            
            try:
                volunteer_id = int(volunteer_text.split("ID: ")[1].split(")")[0])
                camp_id = int(camp_text.split("ID: ")[1].split(")")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Please select valid volunteer and camp")
                return
            
            result = self.volunteer_manager.assign_volunteer_to_camp(volunteer_id, camp_id, role)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_volunteers()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Assign", command=save_assignment, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    def allocate_donation_dialog(self):
        """Dialog to allocate donation to camp"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Allocate Donation")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get pending donations and active camps
        donations = self.donation_manager.get_pending_donations()
        camps = self.camp_manager.get_camps_summary()
        
        # Form fields
        tk.Label(dialog, text="Donation:").pack(pady=5)
        donation_var = tk.StringVar()
        donation_combo = ttk.Combobox(dialog, textvariable=donation_var, 
                                     values=[f"{d['donor_name']} - {d['type_name']} ({d['remaining_quantity']} {d['unit']})" for d in donations])
        donation_combo.pack(pady=5)
        
        tk.Label(dialog, text="Camp:").pack(pady=5)
        camp_var = tk.StringVar()
        camp_combo = ttk.Combobox(dialog, textvariable=camp_var, 
                                 values=[f"{c['camp_name']} (ID: {c['camp_id']})" for c in camps])
        camp_combo.pack(pady=5)
        
        tk.Label(dialog, text="Quantity to Allocate:").pack(pady=5)
        quantity_entry = tk.Entry(dialog, width=40)
        quantity_entry.pack(pady=5)
        
        def save_allocation():
            donation_text = donation_var.get()
            camp_text = camp_var.get()
            quantity = quantity_entry.get()
            
            try:
                donation_id = next(d['donation_id'] for d in donations 
                                 if f"{d['donor_name']} - {d['type_name']}" in donation_text)
                camp_id = int(camp_text.split("ID: ")[1].split(")")[0])
                quantity = int(quantity)
            except (ValueError, StopIteration):
                messagebox.showerror("Error", "Please select valid donation and camp, and enter a valid quantity")
                return
            
            result = self.resource_manager.allocate_donation_to_camp(donation_id, camp_id, quantity)
            
            if result['success']:
                messagebox.showinfo("Success", result['message'])
                dialog.destroy()
                self.refresh_donations()
                self.refresh_resources()
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", result['message'])
        
        save_btn = tk.Button(dialog, text="Allocate", command=save_allocation, bg='#4CAF50', fg='white')
        save_btn.pack(pady=10)
    
    # Refresh methods
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            summary = self.db.get_dashboard_summary()
            
            # Update summary cards
            card_updates = [
                ("Active Disasters", summary['active_disasters']),
                ("Active Camps", summary['active_camps']),
                ("Available Volunteers", summary['available_volunteers']),
                ("Total Occupancy", summary['total_occupancy']),
                ("Critical Shortages", summary['critical_shortages'])
            ]
            
            for title, value in card_updates:
                if title in self.summary_cards:
                    self.summary_cards[title].config(text=str(value))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh dashboard: {str(e)}")
    
    def refresh_disasters(self):
        """Refresh disasters data"""
        try:
            # Clear existing data
            for item in self.disasters_tree.get_children():
                self.disasters_tree.delete(item)
            
            # Load new data
            disasters = self.disaster_manager.get_disasters_summary()
            for disaster in disasters:
                self.disasters_tree.insert('', 'end', values=(
                    disaster['disaster_id'],
                    disaster['disaster_name'],
                    disaster['disaster_type'],
                    disaster['location'],
                    disaster['severity'],
                    disaster['status'],
                    disaster['start_date'],
                    disaster['camp_count']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh disasters: {str(e)}")
    
    def refresh_camps(self):
        """Refresh camps data"""
        try:
            # Clear existing data
            for item in self.camps_tree.get_children():
                self.camps_tree.delete(item)
            
            # Load new data
            camps = self.camp_manager.get_camps_summary()
            for camp in camps:
                self.camps_tree.insert('', 'end', values=(
                    camp['camp_id'],
                    camp['camp_name'],
                    camp['disaster_name'],
                    camp['location'],
                    camp['capacity'],
                    camp['current_occupancy'],
                    f"{camp['occupancy_percentage']}%",
                    camp['capacity_status']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh camps: {str(e)}")
    
    def refresh_resources(self):
        """Refresh resources data"""
        try:
            # Clear existing data
            for item in self.resources_tree.get_children():
                self.resources_tree.delete(item)
            
            # Load shortage data
            shortages = self.resource_manager.get_resource_shortages()
            for shortage in shortages:
                shortage_amount = shortage['quantity_needed'] - shortage['quantity_available']
                status = "Critical" if shortage_amount > shortage['quantity_available'] else "Shortage"
                
                self.resources_tree.insert('', 'end', values=(
                    shortage['camp_name'],
                    shortage['type_name'],
                    shortage['quantity_available'],
                    shortage['quantity_needed'],
                    shortage_amount,
                    status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh resources: {str(e)}")
    
    def refresh_volunteers(self):
        """Refresh volunteers data"""
        try:
            # Clear existing data
            for item in self.volunteers_tree.get_children():
                self.volunteers_tree.delete(item)
            
            # Load new data
            volunteers = self.volunteer_manager.get_volunteers_summary()
            for volunteer in volunteers:
                current_camps = ", ".join(volunteer['current_camps']) if volunteer['current_camps'] else "None"
                
                self.volunteers_tree.insert('', 'end', values=(
                    volunteer['volunteer_id'],
                    f"{volunteer['first_name']} {volunteer['last_name']}",
                    volunteer['email'],
                    volunteer['phone'],
                    volunteer['skills'],
                    volunteer['availability_status'],
                    volunteer['active_assignments']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh volunteers: {str(e)}")
    
    def refresh_donations(self):
        """Refresh donations data"""
        try:
            # Clear existing data
            for item in self.donations_tree.get_children():
                self.donations_tree.delete(item)
            
            # Load new data
            donations = self.donation_manager.get_donations_summary()
            for donation in donations:
                self.donations_tree.insert('', 'end', values=(
                    donation['donation_id'],
                    donation['donor_name'],
                    donation['type_name'],
                    f"{donation['quantity_donated']} {donation['unit']}",
                    donation['status'],
                    donation['donation_date'][:10],
                    f"{donation['remaining_quantity']} {donation['unit']}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh donations: {str(e)}")
    
    # Additional methods
    def show_resource_shortages(self):
        """Show resource shortages in a new window"""
        shortages = self.resource_manager.get_critical_shortages()
        
        if not shortages:
            messagebox.showinfo("No Critical Shortages", "No critical resource shortages found.")
            return
        
        shortage_window = tk.Toplevel(self.root)
        shortage_window.title("Critical Resource Shortages")
        shortage_window.geometry("800x400")
        
        # Create treeview for shortages
        columns = ('Camp', 'Resource', 'Available', 'Needed', 'Shortage', 'Severity')
        shortage_tree = ttk.Treeview(shortage_window, columns=columns, show='headings', height=15)
        
        for col in columns:
            shortage_tree.heading(col, text=col)
            shortage_tree.column(col, width=120)
        
        shortage_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Populate data
        for shortage in shortages:
            shortage_amount = shortage['quantity_needed'] - shortage['quantity_available']
            shortage_tree.insert('', 'end', values=(
                shortage['camp_name'],
                shortage['type_name'],
                shortage['quantity_available'],
                shortage['quantity_needed'],
                shortage_amount,
                shortage.get('shortage_severity', 'High')
            ))
    
    def auto_allocate_donations(self):
        """Auto-allocate donations to camps with shortages"""
        result = self.resource_manager.auto_allocate_donations()
        messagebox.showinfo("Auto-Allocation", result['message'])
        self.refresh_donations()
        self.refresh_resources()
        self.refresh_dashboard()
    
    def generate_comprehensive_report(self):
        """Generate comprehensive system report"""
        try:
            report = "DISASTER RELIEF MANAGEMENT SYSTEM - COMPREHENSIVE REPORT\n"
            report += "=" * 60 + "\n\n"
            
            # Disaster statistics
            disaster_stats = self.disaster_manager.get_disaster_statistics()
            report += "DISASTER STATISTICS:\n"
            report += f"Total Disasters: {disaster_stats['total_disasters']}\n"
            report += f"Active Disasters: {disaster_stats['active_disasters']}\n"
            report += f"Resolved Disasters: {disaster_stats['resolved_disasters']}\n\n"
            
            # Camp statistics
            camp_stats = self.camp_manager.get_camp_statistics()
            report += "CAMP STATISTICS:\n"
            report += f"Total Camps: {camp_stats['total_camps']}\n"
            report += f"Active Camps: {camp_stats['active_camps']}\n"
            report += f"Total Capacity: {camp_stats['total_capacity']}\n"
            report += f"Total Occupancy: {camp_stats['total_occupancy']}\n"
            report += f"Average Occupancy: {camp_stats['average_occupancy']}%\n"
            report += f"Overcrowded Camps: {camp_stats['overcrowded_camps']}\n\n"
            
            # Resource statistics
            resource_stats = self.resource_manager.get_resource_statistics()
            report += "RESOURCE STATISTICS:\n"
            report += f"Total Resource Types: {resource_stats['total_resource_types']}\n"
            report += f"Total Shortages: {resource_stats['total_shortages']}\n"
            report += f"Critical Shortages: {resource_stats['critical_shortages']}\n\n"
            
            # Volunteer statistics
            volunteer_stats = self.volunteer_manager.get_volunteer_statistics()
            report += "VOLUNTEER STATISTICS:\n"
            report += f"Total Volunteers: {volunteer_stats['total_volunteers']}\n"
            report += f"Available Volunteers: {volunteer_stats['available_volunteers']}\n"
            report += f"Assigned Volunteers: {volunteer_stats['assigned_volunteers']}\n"
            report += f"Active Assignments: {volunteer_stats['active_assignments']}\n\n"
            
            # Donation statistics
            donation_stats = self.donation_manager.get_donation_statistics()
            report += "DONATION STATISTICS:\n"
            report += f"Total Donations: {donation_stats['total_donations']}\n"
            report += f"Pending Donations: {donation_stats['pending_donations']}\n"
            report += f"Total Donated Quantity: {donation_stats['total_donated_quantity']}\n\n"
            
            report += "Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Display in reports tab
            self.reports_text.delete(1.0, tk.END)
            self.reports_text.insert(1.0, report)
            
            messagebox.showinfo("Report Generated", "Comprehensive report has been generated and displayed in the Reports tab.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def export_data(self):
        """Export data to CSV files"""
        try:
            # Export disasters
            disasters = self.disaster_manager.get_disasters_summary()
            if disasters:
                df_disasters = pd.DataFrame(disasters)
                df_disasters.to_csv('disasters_export.csv', index=False)
            
            # Export camps
            camps = self.camp_manager.get_camps_summary()
            if camps:
                df_camps = pd.DataFrame(camps)
                df_camps.to_csv('camps_export.csv', index=False)
            
            # Export volunteers
            volunteers = self.volunteer_manager.get_volunteers_summary()
            if volunteers:
                df_volunteers = pd.DataFrame(volunteers)
                df_volunteers.to_csv('volunteers_export.csv', index=False)
            
            # Export donations
            donations = self.donation_manager.get_donations_summary()
            if donations:
                df_donations = pd.DataFrame(donations)
                df_donations.to_csv('donations_export.csv', index=False)
            
            messagebox.showinfo("Export Complete", "Data has been exported to CSV files in the project directory.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def __del__(self):
        """Cleanup database connection"""
        if hasattr(self, 'db'):
            self.db.disconnect()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = DisasterReliefApp(root)
    
    # Handle window close
    def on_closing():
        app.db.disconnect()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
