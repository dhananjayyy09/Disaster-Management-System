-- Insert ONLY the sample data (skip CREATE TABLE statements)
USE disaster_relief_db;

-- Insert sample disaster data (IGNORE if already exists)
INSERT IGNORE INTO disasters (disaster_id, disaster_name, disaster_type, location, severity, start_date, status, description) VALUES
(1, 'Northern Earthquake 2024', 'Earthquake', 'Northern Region', 'High', '2024-01-15', 'Active', 'Major earthquake affecting northern districts'),
(2, 'Coastal Flooding', 'Flood', 'Coastal Areas', 'Medium', '2024-02-01', 'Active', 'Heavy rainfall causing widespread flooding'),
(3, 'Forest Fire West', 'Wildfire', 'Western Forest', 'Critical', '2024-02-10', 'Ongoing', 'Large wildfire spreading rapidly'),
(4, 'Hurricane Season 2024', 'Hurricane', 'Southern Coast', 'High', '2024-03-01', 'Active', 'Major hurricane approaching coastal areas');

-- Insert sample relief camps (IGNORE if already exists)
INSERT IGNORE INTO relief_camps (camp_id, camp_name, disaster_id, location, capacity, current_occupancy, contact_person, contact_phone, status) VALUES
(1, 'North Relief Center', 1, 'Northern District', 500, 320, 'John Smith', '+1234567890', 'Active'),
(2, 'Coastal Shelter', 2, 'Coastal Town', 300, 180, 'Jane Doe', '+1234567891', 'Active'),
(3, 'West Emergency Camp', 3, 'Western Region', 400, 250, 'Bob Johnson', '+1234567892', 'Active'),
(4, 'South Hurricane Shelter', 4, 'Southern City', 600, 450, 'Sarah Williams', '+1234567893', 'Overcrowded');

-- Link coordinator to camps
INSERT IGNORE INTO camp_coordinators (user_id, camp_id) VALUES
(2, 1), -- coordinator1 assigned to North Relief Center
(2, 2); -- coordinator1 assigned to Coastal Shelter

-- Insert sample volunteers
INSERT IGNORE INTO volunteers (volunteer_id, user_id, first_name, last_name, email, phone, skills, availability_status) VALUES
(1, 3, 'Alice', 'Williams', 'alice@email.com', '+1234567893', 'Medical, First Aid', 'Available'),
(2, NULL, 'Charlie', 'Brown', 'charlie@email.com', '+1234567894', 'Logistics, Transportation', 'Available'),
(3, NULL, 'Diana', 'Davis', 'diana@email.com', '+1234567895', 'Food Distribution, Management', 'Available'),
(4, NULL, 'Eve', 'Miller', 'eve@email.com', '+1234567896', 'Communication, Coordination', 'Available'),
(5, NULL, 'Frank', 'Wilson', 'frank@email.com', '+1234567897', 'Medical, Emergency Response', 'Available'),
(6, NULL, 'Grace', 'Taylor', 'grace@email.com', '+1234567898', 'Search and Rescue', 'Available'),
(7, NULL, 'Henry', 'Anderson', 'henry@email.com', '+1234567899', 'Construction', 'Available'),
(8, NULL, 'Iris', 'Martinez', 'iris@email.com', '+1234567900', 'Nursing', 'Available');

-- Insert sample resources for camps
INSERT IGNORE INTO resources (camp_id, resource_type_id, quantity_available, quantity_needed) VALUES
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
('Medical Foundation', 'medical@email.com', 4, 200, 'Received', 'Medical equipment donation'),
('Clothing Drive', 'clothing@email.com', 5, 300, 'Received', 'Winter clothing collection'),
('Tech Company', 'tech@email.com', 7, 10, 'Received', 'Power generators for emergency use'),
('Fuel Corp', 'fuel@email.com', 8, 500, 'Received', 'Emergency fuel supply'),
('Amazon Foundation', 'amazon@charity.com', 1, 1000, 'Received', 'Large food donation'),
('Google.org', 'google@charity.com', 2, 3000, 'Received', 'Water supply'),
('Microsoft', 'microsoft@charity.com', 4, 150, 'Received', 'Medical equipment');

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
(1, 1, 'Medical Coordinator', '2024-01-16', 'Active'),
(2, 2, 'Logistics Officer', '2024-02-02', 'Active'),
(3, 3, 'Food Distribution Manager', '2024-02-11', 'Active');

-- Update volunteer status for assigned volunteers
UPDATE volunteers SET availability_status = 'Assigned' WHERE volunteer_id IN (1, 2, 3);

SELECT 'Sample data inserted successfully!' as Status;
