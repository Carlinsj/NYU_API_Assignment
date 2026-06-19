# NYU AV Operations Dashboard

## Overview

This project is a prototype AV Operations Dashboard built using Python, Streamlit, Google Sheets, and JSON-based device control simulation.

The dashboard integrates two independent spreadsheet data sources into a single interface and demonstrates:

* Spreadsheet integration
* Role-Based Access Control (RBAC)
* JSON payload generation
* Simulated API communication
* Command auditing
* AV workflow automation

The application simulates how an AV operations team could manage equipment inventory, staff schedules, and hardware control actions through a centralized dashboard.

## Spreadsheets
1. https://docs.google.com/spreadsheets/d/1Kn_1_Mmqkv9RlJpRAfI2_luui8UtjwGK6nbvT7Z_Amw/edit
2. https://docs.google.com/spreadsheets/d/1e4QhZNGueIh0dx7qg1yuDfIuDwoPv9hIXmWR-BjDVdo/edit

## Features

### Unified Dashboard

The application combines data from:

* AV Equipment Inventory
* Staff Shift Schedule

Both datasets are displayed in a single dashboard.

### Device Status Monitoring

The dashboard displays device status indicators:

* 🟢 Online
* 🔴 Offline

### Role-Based Access Control

#### Technician

* View inventory
* View schedules
* Filter data
* Cannot trigger commands

#### Manager

* View all data
* Select devices
* Generate commands
* Assign staff members
* View JSON payloads
* View simulated API requests
* Access audit logs

### JSON Device Control

Managers can generate JSON payloads that simulate commands sent to AV hardware.

Example:

```json
{
    "command": "power_on",
    "device": "projector_1",
    "device_id": 1,
    "room": "Room 101",
    "assigned_staff": "Carlin",
    "requested_by_role": "Manager",
    "timestamp": "2026-06-18T15:30:00",
    "target_api_endpoint": "/api/av/device-control",
    "method": "POST"
}
```

### Audit Logging

All generated commands are recorded in an audit log containing:

* Device
* Command
* Assigned Staff
* Timestamp
* Request Method

## Technologies Used

* Python
* Streamlit
* Pandas
* Google Sheets
* JSON
* HTTP API Simulation

## Setup

### Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install streamlit pandas
```

### Run Application

```bash
streamlit run app.py
```

## Testing

### Technician Role

1. Select Technician.
2. Verify inventory and schedules are visible.
3. Verify command controls are not available.

### Manager Role

1. Select Manager.
2. Select a device.
3. Select a command.
4. Assign a staff member.
5. Click **Trigger Device Command**.
6. Verify:

   * JSON payload is generated
   * Simulated HTTP request is displayed
   * Command appears in the audit log

## Assignment Requirements Addressed

* Connect two spreadsheets into a unified UI
* Implement Role-Based Access Control (RBAC)
* Restrict actions based on user role
* Generate valid JSON control payloads
* Simulate AV hardware API communication
* Demonstrate workflow automation
* Maintain command history through audit logging
