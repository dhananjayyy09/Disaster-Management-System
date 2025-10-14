-- Disaster Relief Management System Database Schema
-- Phase 2 Implementation

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    FOREIGN KEY (disaster_id) REFERENCES disasters(disaster_id) ON DELETE CASCADE
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
    FOREIGN KEY (resource_type_id) REFERENCES resource_types(resource_type_id) ON DELETE CASCADE
);

-- Volunteers Table
CREATE TABLE volunteers (
    volunteer_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    skills TEXT,
    availability_status ENUM('Available', 'Assigned', 'Unavailable') DEFAULT 'Available',
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE
);

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
    FOREIGN KEY (resource_type_id) REFERENCES resource_types(resource_type_id) ON DELETE CASCADE
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
    FOREIGN KEY (camp_id) REFERENCES relief_camps(camp_id) ON DELETE CASCADE
);

-- Insert sample resource types
INSERT INTO resource_types (type_name, unit, description) VALUES
('Food', 'kg', 'Non-perishable food items'),
('Water', 'liters', 'Drinking water'),
('Blankets', 'pieces', 'Warm blankets for shelter'),
('Medical Supplies', 'units', 'First aid and medical equipment'),
('Clothing', 'pieces', 'Clothes for affected people'),
('Tents', 'units', 'Emergency shelter tents'),
('Generators', 'units', 'Power generators'),
('Fuel', 'liters', 'Gasoline and diesel fuel');

-- Insert sample disaster data
INSERT INTO disasters (disaster_name, disaster_type, location, severity, start_date, status, description) VALUES
('Northern Earthquake 2024', 'Earthquake', 'Northern Region', 'High', '2024-01-15', 'Active', 'Major earthquake affecting northern districts'),
('Coastal Flooding', 'Flood', 'Coastal Areas', 'Medium', '2024-02-01', 'Active', 'Heavy rainfall causing widespread flooding'),
('Forest Fire West', 'Wildfire', 'Western Forest', 'Critical', '2024-02-10', 'Ongoing', 'Large wildfire spreading rapidly');

-- Insert sample relief camps
INSERT INTO relief_camps (camp_name, disaster_id, location, capacity, current_occupancy, contact_person, contact_phone) VALUES
('North Relief Center', 1, 'Northern District', 500, 320, 'John Smith', '+1234567890'),
('Coastal Shelter', 2, 'Coastal Town', 300, 180, 'Jane Doe', '+1234567891'),
('West Emergency Camp', 3, 'Western Region', 400, 250, 'Bob Johnson', '+1234567892');

-- Insert sample volunteers
INSERT INTO volunteers (first_name, last_name, email, phone, skills, availability_status) VALUES
('Alice', 'Williams', 'alice@email.com', '+1234567893', 'Medical, First Aid', 'Available'),
('Charlie', 'Brown', 'charlie@email.com', '+1234567894', 'Logistics, Transportation', 'Available'),
('Diana', 'Davis', 'diana@email.com', '+1234567895', 'Food Distribution, Management', 'Assigned'),
('Eve', 'Miller', 'eve@email.com', '+1234567896', 'Communication, Coordination', 'Available');

-- Insert sample resources for camps
INSERT INTO resources (camp_id, resource_type_id, quantity_available, quantity_needed) VALUES
(1, 1, 150, 200), -- North Relief Center - Food
(1, 2, 500, 800), -- North Relief Center - Water
(1, 3, 80, 120),  -- North Relief Center - Blankets
(1, 4, 50, 100),  -- North Relief Center - Medical Supplies
(2, 1, 100, 150), -- Coastal Shelter - Food
(2, 2, 300, 500), -- Coastal Shelter - Water
(2, 3, 60, 90),   -- Coastal Shelter - Blankets
(3, 1, 80, 120),  -- West Emergency Camp - Food
(3, 2, 400, 600), -- West Emergency Camp - Water
(3, 6, 20, 50);   -- West Emergency Camp - Tents

-- Insert sample donations
INSERT INTO donations (donor_name, donor_contact, resource_type_id, quantity_donated, status, notes) VALUES
('Red Cross', 'redcross@email.com', 1, 500, 'Received', 'Emergency food supplies'),
('Local Charity', 'charity@email.com', 2, 1000, 'Received', 'Water bottles donation'),
('Medical Foundation', 'medical@email.com', 4, 200, 'Pending', 'Medical equipment donation'),
('Clothing Drive', 'clothing@email.com', 5, 300, 'Received', 'Winter clothing collection');

-- Insert sample volunteer assignments
INSERT INTO volunteer_assignments (volunteer_id, camp_id, role, start_date, status) VALUES
(3, 1, 'Food Distribution Coordinator', '2024-01-16', 'Active'),
(4, 2, 'Communication Officer', '2024-02-02', 'Active');
