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
│ status          │     │ contact_phone    │          │
│ description     │     │ status           │          │
│ created_at      │     │ created_at       │          │
└─────────────────┘     └──────────────────┘          │
       │                      │                       │
       │                      │                       │
       │            ┌──────────────────┐              │
       │            │ VOLUNTEER_ASSIGN │              │
       │            │                  │              │
       │            ├──────────────────┤              │
       │            │ assignment_id PK │              │
       │            │ volunteer_id FK  │              │
       │            │ camp_id FK       │              │
       │            │ role             │              │
       │            │ start_date       │              │
       │            │ end_date         │              │
       │            │ status           │              │
       │            └──────────────────┘              │
       │                       │                      │
       │                       │                      │
┌─────────────────┐            │                ┌─────────────────┐
│   VOLUNTEERS    │◄───────────┘                │ RESOURCE_TYPES  │
├─────────────────┤                             ├─────────────────┤
│ volunteer_id(PK)│                             │ resource_type_id│
│ first_name      │                             │ type_name       │
│ last_name       │                             │ unit            │
│ email           │                             │ description     │
│ phone           │                             └─────────────────┘
│ skills          │                                      │
│ availability    │                                      │
│ registration_dt │                                      │
└─────────────────┘                                      │
                                                         │
┌─────────────────┐           ┌─────────────────┐        │
│   DONATIONS     │           │DONATION_ALLOCAT │        │
├─────────────────┤           ├─────────────────┤        │
│ donation_id (PK)│◄──────────┤ allocation_id PK│        │
│ donor_name      │           │ donation_id (FK)│        │
│ donor_contact   │           │ camp_id (FK)    │        │
│ resource_type_id│───────────┤ quantity_alloc  │        │
│ quantity_donated│           │ allocation_date │        │
│ donation_date   │           │ status          │        │
│ status          │           └─────────────────┘        │
│ notes           │                                      │
└─────────────────┘                                      │
                                                         │
                                                         │
                                                         ▼

Backup Tables:

┌───────────────────────┐     ┌─────────────────────────┐
│   disasters_backup    │     │   relief_camps_backup    │
│ (same columns +       │     │ (same columns +          │
│  backup_timestamp,    │     │  backup_timestamp,       │
│  backup_action)       │     │  backup_action)          │
└───────────────────────┘     └─────────────────────────┘

┌───────────────────────┐     ┌─────────────────────────────┐
│  resources_backup     │     │volunteer_assignments_backup │
│ (same columns +       │     │ (same columns +             │
│  backup_timestamp,    │     │  backup_timestamp,          │
│  backup_action)       │     │  backup_action)             │
└───────────────────────┘     └─────────────────────────────┘

┌───────────────────────┐     ┌─────────────────────────┐
│   volunteers_backup   │     │    donations_backup     │
│ (same columns +       │     │ (same columns +         │
│  backup_timestamp,    │     │  backup_timestamp,      │
│  backup_action)       │     │  backup_action)         │
└───────────────────────┘     └─────────────────────────┘

---

## Table Relationships

1. **DISASTERS ↔ RELIEF_CAMPS (One-to-Many)**
    - One disaster has many relief camps.
    - Foreign key: `relief_camps.disaster_id` references `disasters.disaster_id`.
   
2. **RELIEF_CAMPS ↔ RESOURCES (One-to-Many)**
    - One camp has many resource entries.
    - Foreign key: `resources.camp_id` references `relief_camps.camp_id`.
   
3. **RELIEF_CAMPS ↔ VOLUNTEER_ASSIGNMENTS (One-to-Many)**
    - One camp has many volunteer assignments.
    - Foreign keys: `volunteer_assignments.camp_id` → `relief_camps.camp_id`
   
4. **VOLUNTEERS ↔ VOLUNTEER_ASSIGNMENTS (One-to-Many)**
    - One volunteer may have multiple assignments.
    - Foreign key: `volunteer_assignments.volunteer_id` references `volunteers.volunteer_id`.
   
5. **RESOURCE_TYPES ↔ RESOURCES (One-to-Many)**
    - One resource type applies to many resources.
    - Foreign key: `resources.resource_type_id` → `resource_types.resource_type_id`
   
6. **RESOURCE_TYPES ↔ DONATIONS (One-to-Many)**
    - One resource type can have many donations.
    - Foreign key: `donations.resource_type_id` → `resource_types.resource_type_id`
   
7. **DONATIONS ↔ DONATION_ALLOCATIONS (One-to-Many)**
    - One donation can be allocated to multiple camps.
    - Foreign key: `donation_allocations.donation_id` → `donations.donation_id`
   
8. **RELIEF_CAMPS ↔ DONATION_ALLOCATIONS (One-to-Many)**
    - One camp can receive multiple donation allocations.
    - Foreign key: `donation_allocations.camp_id` → `relief_camps.camp_id`

---

## Key Constraints and Business Rules

- All tables have auto-increment primary keys ensuring uniqueness.
- Foreign key constraints enforce data integrity; cascading deletes are applied where appropriate (e.g., deleting a disaster deletes its camps).
- Unique constraints ensure no duplicated entries for volunteers' emails and resource type names.
- Check constraints limit values (e.g., disaster types, severity levels, status).
- Default timestamps and status values used to track creation and updates.
- Backup tables mirror core tables with additional columns `backup_timestamp` and `backup_action` for audit trails.

---

## Indexes for Performance

- Primary keys are indexed automatically.
- Foreign keys related to disaster, camp, volunteer, resource type, donation efficiently indexed.
- Additional indexes on status, disaster type, availability status, and donation date optimize query speed.

---

## Data Flow and Operations

- Disaster → Camps → Volunteers → Resources flow allows effective tracking of relief operations.
- Donations collected and allocated to camps as per requirement.
- Backup tables automatically updated by triggers on every change.
- Reports aggregated from core tables assist decision making.

---

## Scalability

- Database design supports horizontal (partitioning) and vertical (indexing) scaling.
- Archive tables planned for older data.
- Triggers and backups ensure reliability and disaster recovery readiness.

---

This ER diagram documentation now accurately reflects your current database and backup design, supporting full disaster relief lifecycle management with robust data integrity and audit capabilities.

```