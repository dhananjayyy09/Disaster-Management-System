-- ============================================
-- AUTOMATIC BACKUP TRIGGERS
-- These triggers automatically backup data on INSERT/UPDATE/DELETE
-- Run this after creating backup tables
-- ============================================

USE disaster_relief_db;

-- Drop existing triggers if they exist
DROP TRIGGER IF EXISTS users_after_insert;
DROP TRIGGER IF EXISTS users_after_update;
DROP TRIGGER IF EXISTS users_before_delete;
DROP TRIGGER IF EXISTS disasters_after_insert;
DROP TRIGGER IF EXISTS disasters_after_update;
DROP TRIGGER IF EXISTS disasters_before_delete;
DROP TRIGGER IF EXISTS donations_after_insert;
DROP TRIGGER IF EXISTS donations_after_update;
DROP TRIGGER IF EXISTS volunteers_after_insert;
DROP TRIGGER IF EXISTS volunteers_after_update;
DROP TRIGGER IF EXISTS volunteers_before_delete;
DROP TRIGGER IF EXISTS relief_camps_after_insert;
DROP TRIGGER IF EXISTS relief_camps_after_update;
DROP TRIGGER IF EXISTS relief_camps_before_delete;
DROP TRIGGER IF EXISTS resources_after_insert;
DROP TRIGGER IF EXISTS resources_after_update;

-- ============ USERS TABLE TRIGGERS ============

DELIMITER $$

CREATE TRIGGER users_after_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_backup (
        user_id, username, email, password_hash, role, full_name, phone, 
        is_active, created_at, last_login, backup_action
    )
    VALUES (
        NEW.user_id, NEW.username, NEW.email, NEW.password_hash, NEW.role, 
        NEW.full_name, NEW.phone, NEW.is_active, NEW.created_at, NEW.last_login, 'INSERT'
    );
END$$

CREATE TRIGGER users_after_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_backup (
        user_id, username, email, password_hash, role, full_name, phone, 
        is_active, created_at, last_login, backup_action
    )
    VALUES (
        NEW.user_id, NEW.username, NEW.email, NEW.password_hash, NEW.role, 
        NEW.full_name, NEW.phone, NEW.is_active, NEW.created_at, NEW.last_login, 'UPDATE'
    );
END$$

CREATE TRIGGER users_before_delete
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_backup (
        user_id, username, email, password_hash, role, full_name, phone, 
        is_active, created_at, last_login, backup_action
    )
    VALUES (
        OLD.user_id, OLD.username, OLD.email, OLD.password_hash, OLD.role, 
        OLD.full_name, OLD.phone, OLD.is_active, OLD.created_at, OLD.last_login, 'DELETE'
    );
END$$

-- ============ DISASTERS TABLE TRIGGERS ============

CREATE TRIGGER disasters_after_insert
AFTER INSERT ON disasters
FOR EACH ROW
BEGIN
    INSERT INTO disasters_backup (
        disaster_id, disaster_name, disaster_type, location, severity, 
        start_date, end_date, status, description, created_at, backup_action
    )
    VALUES (
        NEW.disaster_id, NEW.disaster_name, NEW.disaster_type, NEW.location, 
        NEW.severity, NEW.start_date, NEW.end_date, NEW.status, NEW.description, 
        NEW.created_at, 'INSERT'
    );
END$$

CREATE TRIGGER disasters_after_update
AFTER UPDATE ON disasters
FOR EACH ROW
BEGIN
    INSERT INTO disasters_backup (
        disaster_id, disaster_name, disaster_type, location, severity, 
        start_date, end_date, status, description, created_at, backup_action
    )
    VALUES (
        NEW.disaster_id, NEW.disaster_name, NEW.disaster_type, NEW.location, 
        NEW.severity, NEW.start_date, NEW.end_date, NEW.status, NEW.description, 
        NEW.created_at, 'UPDATE'
    );
END$$

CREATE TRIGGER disasters_before_delete
BEFORE DELETE ON disasters
FOR EACH ROW
BEGIN
    INSERT INTO disasters_backup (
        disaster_id, disaster_name, disaster_type, location, severity, 
        start_date, end_date, status, description, created_at, backup_action
    )
    VALUES (
        OLD.disaster_id, OLD.disaster_name, OLD.disaster_type, OLD.location, 
        OLD.severity, OLD.start_date, OLD.end_date, OLD.status, OLD.description, 
        OLD.created_at, 'DELETE'
    );
END$$

-- ============ DONATIONS TABLE TRIGGERS ============

CREATE TRIGGER donations_after_insert
AFTER INSERT ON donations
FOR EACH ROW
BEGIN
    INSERT INTO donations_backup (
        donation_id, donor_name, donor_contact, resource_type_id, 
        quantity_donated, donation_date, status, notes, backup_action
    )
    VALUES (
        NEW.donation_id, NEW.donor_name, NEW.donor_contact, NEW.resource_type_id, 
        NEW.quantity_donated, NEW.donation_date, NEW.status, NEW.notes, 'INSERT'
    );
END$$

CREATE TRIGGER donations_after_update
AFTER UPDATE ON donations
FOR EACH ROW
BEGIN
    INSERT INTO donations_backup (
        donation_id, donor_name, donor_contact, resource_type_id, 
        quantity_donated, donation_date, status, notes, backup_action
    )
    VALUES (
        NEW.donation_id, NEW.donor_name, NEW.donor_contact, NEW.resource_type_id, 
        NEW.quantity_donated, NEW.donation_date, NEW.status, NEW.notes, 'UPDATE'
    );
END$$

-- ============ VOLUNTEERS TABLE TRIGGERS ============

CREATE TRIGGER volunteers_after_insert
AFTER INSERT ON volunteers
FOR EACH ROW
BEGIN
    INSERT INTO volunteers_backup (
        volunteer_id, first_name, last_name, email, phone, skills,
        availability_status, registration_date, backup_action
    )
    VALUES (
        NEW.volunteer_id, NEW.first_name, NEW.last_name, NEW.email, 
        NEW.phone, NEW.skills, NEW.availability_status, 
        NEW.registration_date, 'INSERT'
    );
END$$

CREATE TRIGGER volunteers_after_update
AFTER UPDATE ON volunteers
FOR EACH ROW
BEGIN
    INSERT INTO volunteers_backup (
        volunteer_id, first_name, last_name, email, phone, skills,
        availability_status, registration_date, backup_action
    )
    VALUES (
        NEW.volunteer_id, NEW.first_name, NEW.last_name, NEW.email, 
        NEW.phone, NEW.skills, NEW.availability_status, 
        NEW.registration_date, 'UPDATE'
    );
END$$

CREATE TRIGGER volunteers_before_delete
BEFORE DELETE ON volunteers
FOR EACH ROW
BEGIN
    INSERT INTO volunteers_backup (
        volunteer_id, first_name, last_name, email, phone, skills,
        availability_status, registration_date, backup_action
    )
    VALUES (
        OLD.volunteer_id, OLD.first_name, OLD.last_name, OLD.email, 
        OLD.phone, OLD.skills, OLD.availability_status, 
        OLD.registration_date, 'DELETE'
    );
END$$

-- ============ RELIEF CAMPS TABLE TRIGGERS ============

CREATE TRIGGER relief_camps_after_insert
AFTER INSERT ON relief_camps
FOR EACH ROW
BEGIN
    INSERT INTO relief_camps_backup (
        camp_id, camp_name, disaster_id, location, capacity,
        current_occupancy, status, contact_person, contact_phone,
        created_at, backup_action
    )
    VALUES (
        NEW.camp_id, NEW.camp_name, NEW.disaster_id, NEW.location,
        NEW.capacity, NEW.current_occupancy, NEW.status,
        NEW.contact_person, NEW.contact_phone, NEW.created_at, 'INSERT'
    );
END$$

CREATE TRIGGER relief_camps_after_update
AFTER UPDATE ON relief_camps
FOR EACH ROW
BEGIN
    INSERT INTO relief_camps_backup (
        camp_id, camp_name, disaster_id, location, capacity,
        current_occupancy, status, contact_person, contact_phone,
        created_at, backup_action
    )
    VALUES (
        NEW.camp_id, NEW.camp_name, NEW.disaster_id, NEW.location,
        NEW.capacity, NEW.current_occupancy, NEW.status,
        NEW.contact_person, NEW.contact_phone, NEW.created_at, 'UPDATE'
    );
END$$

CREATE TRIGGER relief_camps_before_delete
BEFORE DELETE ON relief_camps
FOR EACH ROW
BEGIN
    INSERT INTO relief_camps_backup (
        camp_id, camp_name, disaster_id, location, capacity,
        current_occupancy, status, contact_person, contact_phone,
        created_at, backup_action
    )
    VALUES (
        OLD.camp_id, OLD.camp_name, OLD.disaster_id, OLD.location,
        OLD.capacity, OLD.current_occupancy, OLD.status,
        OLD.contact_person, OLD.contact_phone, OLD.created_at, 'DELETE'
    );
END$$

-- ============ RESOURCES TABLE TRIGGERS ============

CREATE TRIGGER resources_after_insert
AFTER INSERT ON resources
FOR EACH ROW
BEGIN
    INSERT INTO resources_backup (
        resource_id, camp_id, resource_type_id, quantity_available,
        quantity_needed, last_updated, backup_action
    )
    VALUES (
        NEW.resource_id, NEW.camp_id, NEW.resource_type_id,
        NEW.quantity_available, NEW.quantity_needed, NEW.last_updated, 'INSERT'
    );
END$$

CREATE TRIGGER resources_after_update
AFTER UPDATE ON resources
FOR EACH ROW
BEGIN
    INSERT INTO resources_backup (
        resource_id, camp_id, resource_type_id, quantity_available,
        quantity_needed, last_updated, backup_action
    )
    VALUES (
        NEW.resource_id, NEW.camp_id, NEW.resource_type_id,
        NEW.quantity_available, NEW.quantity_needed, NEW.last_updated, 'UPDATE'
    );
END$$

DELIMITER ;

-- Success message
SELECT 'All backup triggers created successfully!' AS Status;
