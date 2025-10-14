# Entity-Relationship (ER) Diagram for Disaster Relief Management System

## Database Schema Overview

The Disaster Relief Management System uses a normalized relational database design with 8 core tables that manage the complete disaster relief lifecycle.

## Entity-Relationship Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   DISASTERS     │     │   RELIEF_CAMPS   │     │   RESOURCES     │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ disaster_id (PK)│◄────┤ disaster_id (FK) │◄────┤ camp_id (FK)    │
│ disaster_name   │     │ camp_id (PK)     │     │ resource_id (PK)│
│ disaster_type   │     │ camp_name        │     │ resource_type_id│
│ location        │     │ location         │     │ quantity_avail  │
│ severity        │     │ capacity         │     │ quantity_needed │
│ start_date      │     │ current_occupancy│     │ last_updated    │
│ end_date        │     │ contact_person   │     └─────────────────┘
│ status          │     │ contact_phone    │              │
│ description     │     │ status           │              │
│ created_at      │     │ created_at       │              │
└─────────────────┘     └──────────────────┘              │
         │                        │                       │
         │                        │                       │
         │              ┌──────────────────┐              │
         │              │ VOLUNTEER_ASSIGN │              │
         │              │                  │              │
         │              ├──────────────────┤              │
         │              │ assignment_id(PK)│              │
         │              │ volunteer_id (FK)│              │
         │              │ camp_id (FK)     │              │
         │              │ role             │              │
         │              │ start_date       │              │
         │              │ end_date         │              │
         │              │ status           │              │
         │              └──────────────────┘              │
         │                        │                       │
         │                        │                       │
┌─────────────────┐               │              ┌─────────────────┐
│   VOLUNTEERS    │◄──────────────┘              │ RESOURCE_TYPES  │
├─────────────────┤                              ├─────────────────┤
│ volunteer_id(PK)│                              │ resource_type_id│
│ first_name      │                              │ type_name       │
│ last_name       │                              │ unit            │
│ email           │                              │ description     │
│ phone           │                              └─────────────────┘
│ skills          │                                       │
│ availability    │                                       │
│ registration_dt │                                       │
└─────────────────┘                                       │
                                                          │
┌─────────────────┐              ┌─────────────────┐      │
│   DONATIONS     │              │DONATION_ALLOCAT │      │
├─────────────────┤              ├─────────────────┤      │
│ donation_id (PK)│◄─────────────┤ allocation_id(PK)│      │
│ donor_name      │              │ donation_id (FK)│      │
│ donor_contact   │              │ camp_id (FK)    │      │
│ resource_type_id│──────────────┤ quantity_alloc  │      │
│ quantity_donated│              │ allocation_date │      │
│ donation_date   │              │ status          │      │
│ status          │              └─────────────────┘      │
│ notes           │                                       │
└─────────────────┘                                       │
                                                          │
                                                          │
                                              ┌─────────────────┐
                                              │ RELIEF_CAMPS    │
                                              │ (Referenced)    │
                                              └─────────────────┘
```

## Table Relationships

### 1. DISASTERS ↔ RELIEF_CAMPS (One-to-Many)
- **Relationship**: One disaster can have multiple relief camps
- **Foreign Key**: `relief_camps.disaster_id` → `disasters.disaster_id`
- **Business Rule**: Each camp must be associated with exactly one disaster

### 2. RELIEF_CAMPS ↔ RESOURCES (One-to-Many)
- **Relationship**: One camp can have multiple resource entries
- **Foreign Key**: `resources.camp_id` → `relief_camps.camp_id`
- **Business Rule**: Each resource entry belongs to exactly one camp

### 3. RELIEF_CAMPS ↔ VOLUNTEER_ASSIGNMENTS (One-to-Many)
- **Relationship**: One camp can have multiple volunteer assignments
- **Foreign Key**: `volunteer_assignments.camp_id` → `relief_camps.camp_id`
- **Business Rule**: Volunteers can be assigned to multiple camps over time

### 4. VOLUNTEERS ↔ VOLUNTEER_ASSIGNMENTS (One-to-Many)
- **Relationship**: One volunteer can have multiple assignments
- **Foreign Key**: `volunteer_assignments.volunteer_id` → `volunteers.volunteer_id`
- **Business Rule**: Each assignment belongs to exactly one volunteer

### 5. RESOURCE_TYPES ↔ RESOURCES (One-to-Many)
- **Relationship**: One resource type can be used in multiple camps
- **Foreign Key**: `resources.resource_type_id` → `resource_types.resource_type_id`
- **Business Rule**: Each resource entry must have a defined type

### 6. RESOURCE_TYPES ↔ DONATIONS (One-to-Many)
- **Relationship**: One resource type can have multiple donations
- **Foreign Key**: `donations.resource_type_id` → `resource_types.resource_type_id`
- **Business Rule**: Each donation must specify what type of resource is donated

### 7. DONATIONS ↔ DONATION_ALLOCATIONS (One-to-Many)
- **Relationship**: One donation can be allocated to multiple camps
- **Foreign Key**: `donation_allocations.donation_id` → `donations.donation_id`
- **Business Rule**: Donations can be split across multiple camps

### 8. RELIEF_CAMPS ↔ DONATION_ALLOCATIONS (One-to-Many)
- **Relationship**: One camp can receive multiple donation allocations
- **Foreign Key**: `donation_allocations.camp_id` → `relief_camps.camp_id`
- **Business Rule**: Each allocation goes to exactly one camp

## Key Constraints and Business Rules

### Primary Keys
- All tables have auto-incrementing primary keys
- Ensures unique identification of all records

### Foreign Key Constraints
- **CASCADE DELETE**: Deleting a disaster removes all associated camps
- **RESTRICT DELETE**: Cannot delete resource types with existing resources/donations
- **Data Integrity**: Ensures referential integrity across all relationships

### Unique Constraints
- **Volunteer Email**: Each volunteer must have a unique email address
- **Resource Type Name**: Each resource type must have a unique name

### Check Constraints
- **Disaster Types**: Must be one of: Earthquake, Flood, Wildfire, Hurricane, Tornado, Other
- **Severity Levels**: Must be one of: Low, Medium, High, Critical
- **Status Values**: Each table has predefined status values
- **Non-negative Quantities**: Resource quantities cannot be negative

### Default Values
- **Timestamps**: Created_at fields default to current timestamp
- **Status Fields**: Default to appropriate initial status
- **Occupancy**: Default to 0 for new camps

## Indexes for Performance

### Primary Indexes
- All primary keys are automatically indexed

### Foreign Key Indexes
- `disaster_id` in relief_camps
- `camp_id` in resources and volunteer_assignments
- `volunteer_id` in volunteer_assignments
- `resource_type_id` in resources and donations
- `donation_id` in donation_allocations

### Query Optimization Indexes
- `status` fields for filtering active records
- `disaster_type` for disaster categorization
- `availability_status` for volunteer filtering
- `donation_date` for temporal queries

## Data Flow and Operations

### 1. Disaster Management Flow
```
Create Disaster → Create Relief Camps → Assign Volunteers → Track Resources
```

### 2. Resource Management Flow
```
Record Donations → Detect Shortages → Allocate Resources → Update Inventories
```

### 3. Volunteer Management Flow
```
Register Volunteers → Assign to Camps → Track Performance → Update Availability
```

### 4. Reporting Flow
```
Aggregate Data → Generate Statistics → Create Reports → Export Data
```

## Sample Data Relationships

### Example: Earthquake Disaster Scenario
```
Earthquake (ID: 1)
├── North Relief Center (ID: 1)
│   ├── Food Resources (Available: 150, Needed: 200)
│   ├── Water Resources (Available: 500, Needed: 800)
│   └── Volunteer Assignments
│       └── Alice Williams (Medical Coordinator)
├── South Emergency Camp (ID: 2)
│   ├── Medical Supplies (Available: 50, Needed: 100)
│   └── Volunteer Assignments
│       └── Bob Johnson (Logistics Manager)
└── Donations
    ├── Red Cross Food Donation (1000 kg) → Allocated to Camps
    └── Medical Foundation Supplies (200 units) → Pending Allocation
```

## Normalization Benefits

### 1NF (First Normal Form)
- All attributes contain atomic values
- No repeating groups or arrays

### 2NF (Second Normal Form)
- All non-key attributes fully dependent on primary key
- Eliminates partial dependencies

### 3NF (Third Normal Form)
- No transitive dependencies
- All non-key attributes dependent only on primary key

### BCNF (Boyce-Codd Normal Form)
- Every determinant is a candidate key
- Eliminates anomalies in data modification

## Scalability Considerations

### Horizontal Scaling
- Database can be partitioned by disaster_id or region
- Read replicas for reporting queries

### Vertical Scaling
- Additional indexes for large datasets
- Query optimization for complex joins

### Data Archiving
- Historical data can be moved to archive tables
- Maintains performance for active operations

This ER design provides a solid foundation for the Disaster Relief Management System, ensuring data integrity, performance, and scalability for real-world disaster relief operations.
