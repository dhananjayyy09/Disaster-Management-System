# Disaster Relief Management System

A comprehensive database-driven system for managing disaster relief operations, including disaster tracking, relief camp management, resource allocation, volunteer coordination, and donation tracking.

## 🎯 Project Overview

This system addresses the critical need for efficient disaster relief management by providing:

- **Real-time tracking** of disasters, relief camps, and resources
- **Automated resource allocation** based on camp needs and donations
- **Volunteer management** with skill-based assignment
- **Donation tracking** and allocation to camps with shortages
- **Visual dashboard** for decision-makers to monitor operations
- **Comprehensive reporting** and analytics

## 🏗️ System Architecture

### Database Layer
- **MySQL Database** with normalized schema
- **8 Core Tables**: disasters, relief_camps, resources, resource_types, volunteers, volunteer_assignments, donations, donation_allocations
- **Proper Relationships** with foreign keys and constraints

### Application Layer
- **Python Backend** with modular design
- **Database Manager** for connection and query handling
- **Specialized Managers** for each domain (disaster, camp, resource, volunteer, donation)
- **Tkinter GUI** with tabbed interface

### Key Features
- **Dashboard** with real-time statistics and charts
- **CRUD Operations** for all entities
- **Resource Shortage Detection** and alerts
- **Automated Donation Allocation**
- **Volunteer Assignment** based on skills and availability
- **Comprehensive Reports** and data export

## 📋 Prerequisites

### Software Requirements
- **Python 3.7+**
- **MySQL Server 8.0+**
- **Required Python Packages** (see requirements.txt)

### System Requirements
- **Windows 10/11** (tested)
- **4GB RAM minimum**
- **1GB free disk space**

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DBMS_Project
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
1. **Install MySQL Server** if not already installed
2. **Start MySQL service**
3. **Run the database setup script**:
```bash
python setup_database.py
```

### 4. Configure Database Connection
Edit `database_manager.py` if needed to update database credentials:
```python
def __init__(self, host='localhost', user='root', password='your_password', database='disaster_relief_db'):
```

## 🎮 Usage Guide

### Option 1: Web Application (Recommended) 🌐
```bash
python run_web_app.py
```
This will:
- Check requirements and database
- Start the Flask web server
- Automatically open your browser to `http://localhost:5000`

### Option 2: Desktop Application 🖥️
```bash
python main_app.py
```

### Option 3: Manual Web Server
```bash
python app.py
```
Then open your browser to `http://localhost:5000`

### Web Application Interface 🌐
The web application provides a modern, responsive interface:

#### 1. Dashboard
- **Real-time statistics** with colorful summary cards
- **Interactive charts** using Chart.js:
  - Disaster types distribution (pie chart)
  - Resource shortages by type (bar chart)
  - Volunteer status breakdown (doughnut chart)
  - Donation trends (bar chart)
- **Recent activity** lists for quick overview
- **Quick action buttons** for common tasks

#### 2. Disasters Management
- **View all disasters** in a responsive table
- **Add new disasters** with form validation
- **Disaster statistics** cards
- **Status indicators** with color coding
- **Search and filter** capabilities

#### 3. Relief Camps Management
- **Camp overview** with occupancy progress bars
- **Add new camps** with capacity planning
- **Overcrowding alerts** for camps >95% full
- **Contact information** management
- **Real-time occupancy** tracking

#### 4. Resource Management
- **Critical shortage alerts** prominently displayed
- **Auto-allocation** button for smart distribution
- **Resource shortage** table with severity indicators
- **Camp-specific** resource tracking
- **Allocation history** and impact tracking

#### 5. Volunteer Management
- **Volunteer registration** with skill tracking
- **Assignment management** to specific camps
- **Availability status** tracking
- **Skills summary** and statistics
- **Performance monitoring**

#### 6. Donation Management
- **Donation recording** with resource type selection
- **Pending donations** alerts
- **Allocation tracking** and status updates
- **Donor information** management
- **Impact visualization**

#### 7. Reports & Analytics
- **Comprehensive statistics** overview
- **System performance** metrics
- **Export functionality** (CSV downloads)
- **Trend analysis** and insights
- **Visual data** representation

### Desktop Application Interface 🖥️
The desktop application provides the same functionality with a Tkinter-based GUI:

#### Tabbed Interface
- **Dashboard Tab** - Overview with charts
- **Disasters Tab** - Disaster management
- **Relief Camps Tab** - Camp operations
- **Resources Tab** - Resource tracking
- **Volunteers Tab** - Volunteer coordination
- **Donations Tab** - Donation management
- **Reports Tab** - Analytics and exports

## 🎭 Demo Scenarios

Run simulation scenarios to populate the system with sample data:

```bash
python demo_scenarios.py
```

### Available Scenarios:
1. **Earthquake Simulation** - Creates earthquake disaster with multiple camps and volunteers
2. **Flood Simulation** - Simulates flood disaster with specific resource needs
3. **Volunteer Assignments** - Automatically assigns volunteers to camps
4. **Donation Allocations** - Allocates donations based on resource shortages
5. **Camp Occupancy Updates** - Simulates realistic camp occupancy levels

## 📊 Database Schema

### Core Tables

#### Disasters Table
- `disaster_id` (Primary Key)
- `disaster_name`, `disaster_type`, `location`
- `severity`, `status`, `start_date`, `end_date`
- `description`, `created_at`

#### Relief Camps Table
- `camp_id` (Primary Key)
- `camp_name`, `disaster_id` (Foreign Key)
- `location`, `capacity`, `current_occupancy`
- `contact_person`, `contact_phone`, `status`

#### Resources Table
- `resource_id` (Primary Key)
- `camp_id` (Foreign Key), `resource_type_id` (Foreign Key)
- `quantity_available`, `quantity_needed`
- `last_updated`

#### Volunteers Table
- `volunteer_id` (Primary Key)
- `first_name`, `last_name`, `email`, `phone`
- `skills`, `availability_status`
- `registration_date`

#### Donations Table
- `donation_id` (Primary Key)
- `donor_name`, `donor_contact`
- `resource_type_id` (Foreign Key)
- `quantity_donated`, `status`, `donation_date`

## 🔧 Key Features

### 1. Real-time Monitoring
- **Live dashboard** with updated statistics
- **Automatic shortage detection** for resources
- **Occupancy tracking** for relief camps
- **Status monitoring** for all entities

### 2. Automated Allocation
- **Smart donation allocation** based on camp needs
- **Resource shortage prioritization**
- **Volunteer assignment** based on skills
- **Capacity-based camp management**

### 3. Comprehensive Reporting
- **System-wide analytics** and statistics
- **Export functionality** for external analysis
- **Trend analysis** over time
- **Performance metrics** for operations

### 4. User-friendly Interface
- **Intuitive tabbed design**
- **Form-based data entry**
- **Visual charts** and graphs
- **Error handling** with user feedback

## 🧪 Testing & Validation

### Sample Data
The system comes with **pre-loaded sample data**:
- **3 Active Disasters** (Earthquake, Flood, Wildfire)
- **3 Relief Camps** with varying capacity and occupancy
- **4 Volunteers** with different skills
- **4 Donations** in various states
- **Resource shortages** for demonstration

### Validation Features
- **Input validation** for all forms
- **Database constraint** enforcement
- **Error handling** with user-friendly messages
- **Data integrity** checks

## 📈 Future Enhancements

### Phase 3 Features (Planned)
1. **Web-based Interface** using Flask/Django
2. **Mobile App** for field volunteers
3. **API Integration** with external disaster databases
4. **Advanced Analytics** with machine learning
5. **Real-time Notifications** and alerts
6. **Multi-language Support**
7. **Cloud Deployment** options

### Technical Improvements
1. **Database Optimization** with indexing
2. **Caching Layer** for better performance
3. **Automated Backups** and recovery
4. **Security Enhancements** with authentication
5. **Scalability Improvements** for large-scale operations

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards
- **PEP 8** Python style guide
- **Type hints** for better code clarity
- **Comprehensive docstrings**
- **Error handling** for all operations

## 📞 Support

### Common Issues
1. **Database Connection Errors**
   - Verify MySQL server is running
   - Check database credentials
   - Ensure database exists

2. **Import Errors**
   - Install all required packages: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **GUI Issues**
   - Verify Tkinter installation
   - Check display settings

### Getting Help
- **Documentation**: Check this README and code comments
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions

## 📄 License

This project is developed for educational purposes as part of a DBMS course project.

## 👥 Team

**B.Tech CSE Students**
- Database Design & Implementation
- Python Backend Development
- GUI Interface Design
- Testing & Documentation

---

## 🎯 Project Goals Achieved

✅ **Real-time disaster tracking**  
✅ **Relief camp management**  
✅ **Resource allocation system**  
✅ **Volunteer coordination**  
✅ **Donation tracking**  
✅ **Visual dashboard**  
✅ **Comprehensive reporting**  
✅ **Sample data & simulations**  

This system successfully demonstrates the power of database-driven applications in solving real-world problems in disaster relief management.
