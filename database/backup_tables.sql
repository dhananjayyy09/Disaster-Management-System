-- ============================================
-- MASTER BACKUP TABLES FOR DISASTER RELIEF SYSTEM
-- Run this after creating the main schema
-- ============================================

USE disaster_relief_db;

-- Backup for Users Table
CREATE TABLE IF NOT EXISTS users_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'coordinator', 'volunteer') NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_user_id (user_id),
    INDEX idx_backup_timestamp (backup_timestamp)
);

-- Backup for Disasters Table
CREATE TABLE IF NOT EXISTS disasters_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    disaster_id INT NOT NULL,
    disaster_name VARCHAR(100) NOT NULL,
    disaster_type VARCHAR(50) NOT NULL,
    location VARCHAR(200) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'Active',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_disaster_id (disaster_id)
);

-- Backup for Relief Camps Table
CREATE TABLE IF NOT EXISTS relief_camps_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    camp_id INT NOT NULL,
    camp_name VARCHAR(100) NOT NULL,
    disaster_id INT NOT NULL,
    location VARCHAR(200) NOT NULL,
    capacity INT NOT NULL,
    current_occupancy INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Active',
    contact_person VARCHAR(100),
    contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_camp_id (camp_id)
);

-- Backup for Donations Table
CREATE TABLE IF NOT EXISTS donations_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT NOT NULL,
    donor_name VARCHAR(100) NOT NULL,
    donor_contact VARCHAR(100),
    resource_type_id INT NOT NULL,
    quantity_donated INT NOT NULL,
    donation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending',
    notes TEXT,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_donation_id (donation_id)
);

-- Backup for Volunteers Table
CREATE TABLE IF NOT EXISTS volunteers_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    skills TEXT,
    availability_status VARCHAR(20) DEFAULT 'Available',
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_volunteer_id (volunteer_id)
);

-- Backup for Resources Table
CREATE TABLE IF NOT EXISTS resources_backup (
    backup_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_id INT NOT NULL,
    camp_id INT NOT NULL,
    resource_type_id INT NOT NULL,
    quantity_available INT DEFAULT 0,
    quantity_needed INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    backup_action ENUM('INSERT', 'UPDATE', 'DELETE', 'MANUAL') DEFAULT 'INSERT',
    INDEX idx_resource_id (resource_id)
);

-- Success message
SELECT 'Backup tables created successfully!' AS Status;
