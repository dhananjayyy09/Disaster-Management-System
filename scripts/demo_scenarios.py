"""
Demo Scenarios for Disaster Relief Management System
This script provides simulation scenarios for demonstration purposes
"""

from database_manager import DatabaseManager
from disaster_manager import DisasterManager
from camp_manager import CampManager
from resource_manager import ResourceManager
from volunteer_manager import VolunteerManager
from donation_manager import DonationManager
import random
from datetime import datetime, timedelta

class DemoScenarios:
    def __init__(self):
        self.db = DatabaseManager()
        self.disaster_manager = DisasterManager(self.db)
        self.camp_manager = CampManager(self.db)
        self.resource_manager = ResourceManager(self.db)
        self.volunteer_manager = VolunteerManager(self.db)
        self.donation_manager = DonationManager(self.db)
        
    def connect(self):
        """Connect to database"""
        return self.db.connect()
    
    def disconnect(self):
        """Disconnect from database"""
        self.db.disconnect()
    
    def simulate_earthquake_scenario(self):
        """Simulate an earthquake disaster scenario"""
        print("🌍 Simulating Earthquake Disaster Scenario...")
        
        # Create earthquake disaster
        result = self.disaster_manager.create_disaster(
            name="Metro City Earthquake",
            disaster_type="Earthquake",
            location="Metro City",
            severity="Critical",
            description="7.2 magnitude earthquake causing widespread damage to infrastructure"
        )
        print(f"  - Created disaster: {result['message']}")
        
        # Create relief camps
        disasters = self.disaster_manager.get_disasters_summary()
        earthquake = next(d for d in disasters if "Metro City Earthquake" in d['disaster_name'])
        
        camps_data = [
            ("Central Relief Camp", earthquake['disaster_id'], "Downtown Metro", 800, "Sarah Johnson", "+1234567890"),
            ("North District Camp", earthquake['disaster_id'], "North District", 600, "Mike Chen", "+1234567891"),
            ("Emergency Shelter", earthquake['disaster_id'], "East Side", 400, "Lisa Rodriguez", "+1234567892")
        ]
        
        for camp_name, disaster_id, location, capacity, contact, phone in camps_data:
            result = self.camp_manager.create_camp(camp_name, disaster_id, location, capacity, contact, phone)
            print(f"  - Created camp: {camp_name}")
        
        # Add volunteers with relevant skills
        volunteers_data = [
            ("Emergency", "Responder", "emergency@email.com", "+1234567893", "Search & Rescue, Medical"),
            ("Fire", "Chief", "fire@email.com", "+1234567894", "Emergency Response, Leadership"),
            ("Medical", "Nurse", "medical@email.com", "+1234567895", "First Aid, Trauma Care"),
            ("Logistics", "Coordinator", "logistics@email.com", "+1234567896", "Supply Chain, Transportation")
        ]
        
        for first_name, last_name, email, phone, skills in volunteers_data:
            result = self.volunteer_manager.register_volunteer(first_name, last_name, email, phone, skills)
            print(f"  - Registered volunteer: {first_name} {last_name}")
        
        # Simulate resource shortages
        camps = self.camp_manager.get_camps_summary()
        earthquake_camps = [c for c in camps if c['disaster_id'] == earthquake['disaster_id']]
        
        resource_types = self.db.get_resource_type_list()
        
        # Create resource entries with shortages
        for camp in earthquake_camps:
            for resource_type in resource_types[:5]:  # First 5 resource types
                available = random.randint(10, 50)
                needed = random.randint(60, 100)
                
                self.resource_manager.create_resource_for_camp(
                    camp['camp_id'], 
                    resource_type['resource_type_id'], 
                    available, 
                    needed
                )
        
        print("  - Created resource shortages for earthquake camps")
        
        # Record donations
        donation_scenarios = [
            ("Red Cross", "redcross@email.com", 1, 1000, "Emergency food supplies"),
            ("Water Aid", "wateraid@email.com", 2, 2000, "Clean drinking water"),
            ("Medical Foundation", "medical@email.com", 4, 500, "Emergency medical supplies"),
            ("Shelter Network", "shelter@email.com", 6, 100, "Emergency tents")
        ]
        
        for donor, contact, resource_type_id, quantity, notes in donation_scenarios:
            result = self.donation_manager.record_donation(donor, contact, resource_type_id, quantity, notes)
            print(f"  - Recorded donation: {quantity} units from {donor}")
        
        print("✅ Earthquake scenario simulation completed!")
    
    def simulate_flood_scenario(self):
        """Simulate a flood disaster scenario"""
        print("🌊 Simulating Flood Disaster Scenario...")
        
        # Create flood disaster
        result = self.disaster_manager.create_disaster(
            name="River Valley Flooding",
            disaster_type="Flood",
            location="River Valley",
            severity="High",
            description="Heavy rainfall causing river overflow and widespread flooding"
        )
        print(f"  - Created disaster: {result['message']}")
        
        # Create relief camps
        disasters = self.disaster_manager.get_disasters_summary()
        flood = next(d for d in disasters if "River Valley Flooding" in d['disaster_name'])
        
        camps_data = [
            ("Riverside Shelter", flood['disaster_id'], "Riverside District", 300, "Tom Wilson", "+1234567897"),
            ("High Ground Camp", flood['disaster_id'], "High Ground Area", 250, "Emma Davis", "+1234567898")
        ]
        
        for camp_name, disaster_id, location, capacity, contact, phone in camps_data:
            result = self.camp_manager.create_camp(camp_name, disaster_id, location, capacity, contact, phone)
            print(f"  - Created camp: {camp_name}")
        
        # Add volunteers with flood-specific skills
        volunteers_data = [
            ("Boat", "Operator", "boat@email.com", "+1234567899", "Water Rescue, Navigation"),
            ("Flood", "Specialist", "flood@email.com", "+1234567800", "Flood Response, Evacuation"),
            ("Community", "Organizer", "community@email.com", "+1234567801", "Community Outreach, Coordination")
        ]
        
        for first_name, last_name, email, phone, skills in volunteers_data:
            result = self.volunteer_manager.register_volunteer(first_name, last_name, email, phone, skills)
            print(f"  - Registered volunteer: {first_name} {last_name}")
        
        # Simulate flood-specific resource needs
        camps = self.camp_manager.get_camps_summary()
        flood_camps = [c for c in camps if c['disaster_id'] == flood['disaster_id']]
        
        # Focus on flood-specific resources
        flood_resources = [
            (2, "Water"), (3, "Blankets"), (5, "Clothing"), (6, "Tents")
        ]
        
        for camp in flood_camps:
            for resource_type_id, _ in flood_resources:
                available = random.randint(20, 40)
                needed = random.randint(80, 120)
                
                self.resource_manager.create_resource_for_camp(
                    camp['camp_id'], 
                    resource_type_id, 
                    available, 
                    needed
                )
        
        print("  - Created flood-specific resource shortages")
        
        # Record flood-specific donations
        flood_donations = [
            ("Water Relief Fund", "water@email.com", 2, 1500, "Clean water bottles"),
            ("Warm Clothes Drive", "clothes@email.com", 5, 800, "Winter clothing"),
            ("Emergency Blankets", "blankets@email.com", 3, 400, "Warm blankets")
        ]
        
        for donor, contact, resource_type_id, quantity, notes in flood_donations:
            result = self.donation_manager.record_donation(donor, contact, resource_type_id, quantity, notes)
            print(f"  - Recorded donation: {quantity} units from {donor}")
        
        print("✅ Flood scenario simulation completed!")
    
    def simulate_volunteer_assignments(self):
        """Simulate volunteer assignments to camps"""
        print("👥 Simulating Volunteer Assignments...")
        
        # Get available volunteers and active camps
        volunteers = self.volunteer_manager.get_available_volunteers_by_skill()
        camps = self.camp_manager.get_camps_summary()
        active_camps = [c for c in camps if c['status'] == 'Active']
        
        if not volunteers or not active_camps:
            print("  - No available volunteers or camps for assignment")
            return
        
        # Assign volunteers to camps
        assignments = [
            ("Search & Rescue Coordinator", "Medical Coordinator", "Food Distribution Manager"),
            ("Emergency Response Lead", "Communication Officer", "Logistics Manager"),
            ("Water Rescue Specialist", "Community Outreach", "Supply Coordinator")
        ]
        
        assigned_count = 0
        for i, volunteer in enumerate(volunteers[:min(9, len(volunteers))]):
            camp = active_camps[i % len(active_camps)]
            role_group = assignments[i // 3]
            role = role_group[i % 3]
            
            result = self.volunteer_manager.assign_volunteer_to_camp(
                volunteer['volunteer_id'], 
                camp['camp_id'], 
                role
            )
            
            if result['success']:
                assigned_count += 1
                print(f"  - Assigned {volunteer['first_name']} {volunteer['last_name']} to {camp['camp_name']} as {role}")
        
        print(f"✅ Assigned {assigned_count} volunteers to camps!")
    
    def simulate_donation_allocations(self):
        """Simulate automatic donation allocations"""
        print("📦 Simulating Donation Allocations...")
        
        # Get pending donations and resource shortages
        pending_donations = self.donation_manager.get_pending_donations()
        shortages = self.resource_manager.get_resource_shortages()
        
        if not pending_donations:
            print("  - No pending donations to allocate")
            return
        
        allocated_count = 0
        for donation in pending_donations:
            # Find camps with shortages for this resource type
            relevant_shortages = [s for s in shortages if s['resource_type_id'] == donation['resource_type_id']]
            
            if relevant_shortages:
                # Allocate to the camp with highest need
                shortage = max(relevant_shortages, key=lambda x: x['quantity_needed'] - x['quantity_available'])
                allocation_amount = min(donation['remaining_quantity'], shortage['quantity_needed'] - shortage['quantity_available'])
                
                if allocation_amount > 0:
                    result = self.resource_manager.allocate_donation_to_camp(
                        donation['donation_id'], 
                        shortage['camp_id'], 
                        allocation_amount
                    )
                    
                    if result['success']:
                        allocated_count += 1
                        print(f"  - Allocated {allocation_amount} {donation['unit']} {donation['type_name']} to {shortage['camp_name']}")
        
        print(f"✅ Allocated {allocated_count} donations to camps!")
    
    def simulate_camp_occupancy_updates(self):
        """Simulate realistic camp occupancy updates"""
        print("🏕️ Simulating Camp Occupancy Updates...")
        
        camps = self.camp_manager.get_camps_summary()
        active_camps = [c for c in camps if c['status'] == 'Active']
        
        updated_count = 0
        for camp in active_camps:
            # Simulate realistic occupancy (70-95% of capacity)
            new_occupancy = random.randint(int(camp['capacity'] * 0.7), int(camp['capacity'] * 0.95))
            
            result = self.camp_manager.update_camp_occupancy(camp['camp_id'], new_occupancy)
            
            if result['success']:
                updated_count += 1
                occupancy_pct = (new_occupancy / camp['capacity']) * 100
                print(f"  - Updated {camp['camp_name']} occupancy to {new_occupancy}/{camp['capacity']} ({occupancy_pct:.1f}%)")
        
        print(f"✅ Updated occupancy for {updated_count} camps!")
    
    def run_full_simulation(self):
        """Run complete simulation with all scenarios"""
        print("🚀 Running Complete Disaster Relief Simulation")
        print("=" * 50)
        
        if not self.connect():
            print("❌ Failed to connect to database")
            return
        
        try:
            # Run all simulation scenarios
            self.simulate_earthquake_scenario()
            print()
            
            self.simulate_flood_scenario()
            print()
            
            self.simulate_volunteer_assignments()
            print()
            
            self.simulate_donation_allocations()
            print()
            
            self.simulate_camp_occupancy_updates()
            print()
            
            print("🎉 Complete simulation finished successfully!")
            print("You can now run the main application to see the populated data.")
            
        except Exception as e:
            print(f"❌ Error during simulation: {str(e)}")
        finally:
            self.disconnect()
    
    def generate_system_report(self):
        """Generate a comprehensive system report"""
        print("📊 Generating System Report")
        print("=" * 30)
        
        if not self.connect():
            print("❌ Failed to connect to database")
            return
        
        try:
            # Get statistics from all managers
            disaster_stats = self.disaster_manager.get_disaster_statistics()
            camp_stats = self.camp_manager.get_camp_statistics()
            resource_stats = self.resource_manager.get_resource_statistics()
            volunteer_stats = self.volunteer_manager.get_volunteer_statistics()
            donation_stats = self.donation_manager.get_donation_statistics()
            
            print(f"📈 SYSTEM OVERVIEW:")
            print(f"  Disasters: {disaster_stats['total_disasters']} total ({disaster_stats['active_disasters']} active)")
            print(f"  Relief Camps: {camp_stats['total_camps']} total ({camp_stats['active_camps']} active)")
            print(f"  Volunteers: {volunteer_stats['total_volunteers']} total ({volunteer_stats['available_volunteers']} available)")
            print(f"  Donations: {donation_stats['total_donations']} total")
            print(f"  Resource Shortages: {resource_stats['total_shortages']} total ({resource_stats['critical_shortages']} critical)")
            
            print(f"\n🏕️ CAMP OCCUPANCY:")
            print(f"  Total Capacity: {camp_stats['total_capacity']}")
            print(f"  Total Occupancy: {camp_stats['total_occupancy']}")
            print(f"  Average Occupancy: {camp_stats['average_occupancy']}%")
            print(f"  Overcrowded Camps: {camp_stats['overcrowded_camps']}")
            
            print(f"\n👥 VOLUNTEER ASSIGNMENTS:")
            print(f"  Active Assignments: {volunteer_stats['active_assignments']}")
            print(f"  Completed Assignments: {volunteer_stats['completed_assignments']}")
            
            print(f"\n📦 DONATION STATUS:")
            print(f"  Pending: {donation_stats['pending_donations']}")
            print(f"  Received: {donation_stats['received_donations']}")
            print(f"  Allocated: {donation_stats['allocated_donations']}")
            
        except Exception as e:
            print(f"❌ Error generating report: {str(e)}")
        finally:
            self.disconnect()

def main():
    """Main function for demo scenarios"""
    demo = DemoScenarios()
    
    print("Disaster Relief Management System - Demo Scenarios")
    print("=" * 50)
    print("1. Run Full Simulation")
    print("2. Generate System Report")
    print("3. Exit")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == "1":
        demo.run_full_simulation()
    elif choice == "2":
        demo.generate_system_report()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
