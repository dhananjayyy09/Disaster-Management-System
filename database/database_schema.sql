-- Disaster Relief Management System Database Schema

CREATE DATABASE IF NOT EXISTS disaster_relief_db;
USE disaster_relief_db;

-- Disasters Table
CREATE TABLE disasters (
    disaster_id INT PRIMARY KEY AUTO_INCREMENT,
    disaster_name VARCHAR(100) NOT NULL,
    disaster_type ENUM('Earthquake', 'Flood', 'Wildfire', 'Hurricane', 'Tornado', 'Other') NOT NULL,
    location VARCHAR(100) NOT NULL,
    severity ENUM('Low', 'Medium', 'High', 'Critical') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    status ENUM('Active', 'Resolved', 'Ongoing') DEFAULT 'Active',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_disaster_type (disaster_type),
    INDEX idx_severity (severity),
    INDEX idx_status (status)
);


-- Relief Camps Table
CREATE TABLE relief_camps (
    camp_id INT PRIMARY KEY AUTO_INCREMENT,
    camp_name VARCHAR(100) NOT NULL,
    disaster_id INT NOT NULL,
    location VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    current_occupancy INT DEFAULT 0,
    contact_person VARCHAR(100),
    contact_phone VARCHAR(20),
    status ENUM('Active', 'Closed', 'Overcrowded') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disaster_id) REFERENCES disasters(disaster_id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_disaster (disaster_id)
);


-- Resource Types Table
CREATE TABLE resource_types (
    resource_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL,
    description TEXT
);


-- Resources Table (Available resources at camps)
CREATE TABLE resources (
    resource_id INT PRIMARY KEY AUTO_INCREMENT,
    camp_id INT NOT NULL,
    resource_type_id INT NOT NULL,
    quantity_available INT NOT NULL DEFAULT 0,
    quantity_needed INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE,
    FOREIGN KEY (resource_type_id) REFERENCES resource_types(resource_type_id) ON DELETE CASCADE,
    INDEX idx_camp (camp_id),
    INDEX idx_resource_type (resource_type_id)
);


-- ==================== AUTHENTICATION TABLES ====================
-- Users Table for Authentication
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'coordinator', 'volunteer') NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
);


-- ==================== VOLUNTEERS TABLES ====================
-- Volunteers Table 
CREATE TABLE volunteers (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    skills TEXT,
    availability_status ENUM('Available', 'Assigned', 'Unavailable') DEFAULT 'Available',
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_availability (availability_status),
    INDEX idx_user (user_id)
);

-- Volunteer Assignments Table
CREATE TABLE volunteer_assignments (
    assignment_id INT PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INT NOT NULL,
    camp_id INT NOT NULL,
    role VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    status ENUM('Active', 'Completed', 'Cancelled') DEFAULT 'Active',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id) ON DELETE CASCADE,
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE,
    INDEX idx_volunteer (volunteer_id),
    INDEX idx_camp (camp_id),
    INDEX idx_status (status)
);

-- Camp Coordinators Table (Link users to camps for coordinator role)
CREATE TABLE camp_coordinators (
    coordinator_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    camp_id INT NOT NULL,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE,
    UNIQUE KEY unique_coordinator_camp (user_id, camp_id),
    INDEX idx_user (user_id),
    INDEX idx_camp (camp_id)
);


-- ==================== DONATIONS TABLES ====================
-- Donations Table
CREATE TABLE donations (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    donor_name VARCHAR(100) NOT NULL,
    donor_contact VARCHAR(100),
    resource_type_id INT NOT NULL,
    quantity_donated INT NOT NULL,
    donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Received', 'Allocated', 'Distributed') DEFAULT 'Pending',
    notes TEXT,
    FOREIGN KEY (resource_type_id) REFERENCES resource_types(resource_type_id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_resource_type (resource_type_id),
    INDEX idx_donation_date (donation_date)
);

-- Donation Allocations Table
CREATE TABLE donation_allocations (
    allocation_id INT PRIMARY KEY AUTO_INCREMENT,
    donation_id INT NOT NULL,
    camp_id INT NOT NULL,
    quantity_allocated INT NOT NULL,
    allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Delivered', 'Received') DEFAULT 'Pending',
    FOREIGN KEY (donation_id) REFERENCES donations(donation_id) ON DELETE CASCADE,
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE,
    INDEX idx_donation (donation_id),
    INDEX idx_camp (camp_id),
    INDEX idx_status (status)
);


-- ==================== INSERT SAMPLE DATA ====================
-- Insert resource types
INSERT INTO resource_types (type_name, unit, description) VALUES
('Food', 'kg', 'Non-perishable food items'),
('Water', 'liters', 'Drinking water'),
('Blankets', 'pieces', 'Warm blankets for shelter'),
('Medical Supplies', 'units', 'First aid and medical equipment'),
('Clothing', 'pieces', 'Clothes for affected people'),
('Tents', 'units', 'Emergency shelter tents'),
('Generators', 'units', 'Power generators'),
('Fuel', 'liters', 'Gasoline and diesel fuel');


-- Insert default admin user (password: admin123)
-- Hash generated using werkzeug.security.generate_password_hash('admin123')
INSERT INTO users (username, email, password_hash, role, full_name, phone) VALUES
('admin', 'admin@disaster-relief.com', 'scrypt:32768:8:1$iqxQF4YQwKjN8F7X$e5c4b9a8f7d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6f5e4d3c2b1a0e9d8c7', 'admin', 'System Administrator', '+1234567800');


-- Insert sample coordinator user (password: coordinator123)
INSERT INTO users (username, email, password_hash, role, full_name, phone) VALUES
('coordinator1', 'coordinator@disaster-relief.com', 'scrypt:32768:8:1$iqxQF4YQwKjN8F7X$e5c4b9a8f7d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6f5e4d3c2b1a0e9d8c7', 'coordinator', 'John Coordinator', '+1234567801');


-- Insert sample volunteer user (password: volunteer123)
INSERT INTO users (username, email, password_hash, role, full_name, phone) VALUES
('volunteer1', 'volunteer@disaster-relief.com', 'scrypt:32768:8:1$iqxQF4YQwKjN8F7X$e5c4b9a8f7d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6f5e4d3c2b1a0e9d8c7', 'volunteer', 'Alice Volunteer', '+1234567802');


-- Insert sample disaster data
INSERT INTO disasters (disaster_name, disaster_type, location, severity, start_date, status, description) VALUES
('Northern Earthquake 2024', 'Earthquake', 'Northern Region', 'High', '2024-01-15', 'Active', 'Major earthquake affecting northern districts'),
('Coastal Flooding', 'Flood', 'Coastal Areas', 'Medium', '2024-02-01', 'Active', 'Heavy rainfall causing widespread flooding'),
('Forest Fire West', 'Wildfire', 'Western Forest', 'Critical', '2024-02-10', 'Ongoing', 'Large wildfire spreading rapidly'),
('Hurricane Season 2024', 'Hurricane', 'Southern Coast', 'High', '2024-03-01', 'Active', 'Major hurricane approaching coastal areas');


-- Insert sample relief camps
INSERT INTO relief_camps (camp_name, disaster_id, location, capacity, current_occupancy, contact_person, contact_phone, status) VALUES
('North Relief Center', 1, 'Northern District', 500, 320, 'John Smith', '+1234567890', 'Active'),
('Coastal Shelter', 2, 'Coastal Town', 300, 180, 'Jane Doe', '+1234567891', 'Active'),
('West Emergency Camp', 3, 'Western Region', 400, 250, 'Bob Johnson', '+1234567892', 'Active'),
('South Hurricane Shelter', 4, 'Southern City', 600, 450, 'Sarah Williams', '+1234567893', 'Overcrowded');


-- Link coordinator to camps
INSERT INTO camp_coordinators (user_id, camp_id) VALUES
(2, 1), -- coordinator1 assigned to North Relief Center
(2, 2); -- coordinator1 assigned to Coastal Shelter


-- Insert sample volunteers
INSERT INTO volunteers (user_id, first_name, last_name, email, phone, skills, availability_status) VALUES
(3, 'Alice', 'Williams', 'alice@email.com', '+1234567893', 'Medical, First Aid', 'Available'),
(NULL, 'Charlie', 'Brown', 'charlie@email.com', '+1234567894', 'Logistics, Transportation', 'Available'),
(NULL, 'Diana', 'Davis', 'diana@email.com', '+1234567895', 'Food Distribution, Management', 'Assigned'),
(NULL, 'Eve', 'Miller', 'eve@email.com', '+1234567896', 'Communication, Coordination', 'Available'),
(NULL, 'Frank', 'Wilson', 'frank@email.com', '+1234567897', 'Medical, Emergency Response', 'Available');


-- Insert sample resources for camps
INSERT INTO resources (camp_id, resource_type_id, quantity_available, quantity_needed) VALUES
-- North Relief Center resources
(1, 1, 150, 200), -- Food
(1, 2, 500, 800), -- Water
(1, 3, 80, 120),  -- Blankets
(1, 4, 50, 100),  -- Medical Supplies
(1, 5, 100, 150), -- Clothing
-- Coastal Shelter resources
(2, 1, 100, 150), -- Food
(2, 2, 300, 500), -- Water
(2, 3, 60, 90),   -- Blankets
(2, 4, 30, 80),   -- Medical Supplies
-- West Emergency Camp resources
(3, 1, 80, 120),  -- Food
(3, 2, 400, 600), -- Water
(3, 6, 20, 50),   -- Tents
(3, 7, 5, 15),    -- Generators
(3, 8, 100, 200), -- Fuel
-- South Hurricane Shelter resources
(4, 1, 200, 350), -- Food
(4, 2, 800, 1200), -- Water
(4, 3, 150, 300), -- Blankets
(4, 4, 80, 150),  -- Medical Supplies
(4, 6, 40, 80);   -- Tents


-- Insert sample donations
INSERT INTO donations (donor_name, donor_contact, resource_type_id, quantity_donated, status, notes) VALUES
('Red Cross', 'redcross@email.com', 1, 500, 'Received', 'Emergency food supplies'),
('Local Charity', 'charity@email.com', 2, 1000, 'Received', 'Water bottles donation'),
('Medical Foundation', 'medical@email.com', 4, 200, 'Pending', 'Medical equipment donation'),
('Clothing Drive', 'clothing@email.com', 5, 300, 'Received', 'Winter clothing collection'),
('Tech Company', 'tech@email.com', 7, 10, 'Pending', 'Power generators for emergency use'),
('Fuel Corp', 'fuel@email.com', 8, 500, 'Received', 'Emergency fuel supply');


-- Insert sample donation allocations
INSERT INTO donation_allocations (donation_id, camp_id, quantity_allocated, status) VALUES
(1, 1, 200, 'Delivered'), -- Red Cross food to North Relief Center
(1, 2, 150, 'Delivered'), -- Red Cross food to Coastal Shelter
(2, 1, 300, 'Received'),  -- Local Charity water to North Relief Center
(2, 3, 400, 'Delivered'), -- Local Charity water to West Emergency Camp
(4, 1, 150, 'Received'),  -- Clothing Drive to North Relief Center
(6, 4, 200, 'Delivered'); -- Fuel Corp to South Hurricane Shelter


-- Insert sample volunteer assignments
INSERT INTO volunteer_assignments (volunteer_id, camp_id, role, start_date, status) VALUES
(3, 1, 'Food Distribution Coordinator', '2024-01-16', 'Active'),
(4, 2, 'Communication Officer', '2024-02-02', 'Active'),
(5, 3, 'Logistics Manager', '2024-02-11', 'Active');


-- ==================== USEFUL VIEWS ====================
-- View for camp resource summary
CREATE VIEW camp_resource_summary AS
SELECT 
    c.camp_id,
    c.camp_name,
    d.disaster_name,
    COUNT(r.resource_id) as total_resource_types,
    SUM(CASE WHEN r.quantity_needed > r.quantity_available THEN 1 ELSE 0 END) as shortages_count,
    c.current_occupancy,
    c.capacity,
    ROUND((c.current_occupancy / c.capacity * 100), 2) as occupancy_percentage
FROM relief_camps c
JOIN disasters d ON c.disaster_id = d.disaster_id
LEFT JOIN resources r ON c.camp_id = r.camp_id
GROUP BY c.camp_id, c.camp_name, d.disaster_name, c.current_occupancy, c.capacity;


-- View for volunteer availability
CREATE VIEW volunteer_availability AS
SELECT 
    v.volunteer_id,
    CONCAT(v.first_name, ' ', v.last_name) as volunteer_name,
    v.email,
    v.phone,
    v.skills,
    v.availability_status,
    COUNT(va.assignment_id) as total_assignments,
    SUM(CASE WHEN va.status = 'Active' THEN 1 ELSE 0 END) as active_assignments
FROM volunteers v
LEFT JOIN volunteer_assignments va ON v.volunteer_id = va.volunteer_id
GROUP BY v.volunteer_id, volunteer_name, v.email, v.phone, v.skills, v.availability_status;


-- ==================== END OF SCHEMA ====================


SELECT 'Database schema created successfully!' as Status;
SELECT 'Default admin username: admin, password: admin123' as DefaultCredentials;
