import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="NYU AV Dashboard", layout="wide")

# Google Sheet CSV links
inventory_url = "https://docs.google.com/spreadsheets/d/1Kn_1_Mmqkv9RlJpRAfI2_luui8UtjwGK6nbvT7Z_Amw/gviz/tq?tqx=out:csv&sheet=AV%20Inventory"
schedule_url = "https://docs.google.com/spreadsheets/d/1e4QhZNGueIh0dx7qg1yuDfIuDwoPv9hIXmWR-BjDVdo/gviz/tq?tqx=out:csv&sheet=Staff%20Schedule"

inventory = pd.read_csv(inventory_url)
schedule = pd.read_csv(schedule_url)

# Keep command history while the app is running
if "command_log" not in st.session_state:
    st.session_state.command_log = []

status_icon = {
    "online": "🟢",
    "offline": "🔴"
}

st.title("NYU AV Operations Dashboard")
st.write("A small prototype for viewing AV inventory, staff schedules, and simulated device commands.")

role = st.selectbox("Select role", ["Technician", "Manager"])

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Devices", len(inventory))

with col2:
    online_count = len(inventory[inventory["Status"].str.lower() == "online"])
    st.metric("Online Devices", online_count)

with col3:
    st.metric("Scheduled Staff", len(schedule))

st.divider()

st.subheader("Operations View")

left_col, right_col = st.columns(2)

with left_col:
    st.write("### AV Equipment Inventory")

    status_options = ["All"] + sorted(inventory["Status"].unique().tolist())
    selected_status = st.selectbox("Filter devices by status", status_options)

    if selected_status == "All":
        visible_inventory = inventory.copy()
    else:
        visible_inventory = inventory[inventory["Status"] == selected_status]

    st.dataframe(visible_inventory, use_container_width=True)

    st.write("### Device Status")

    for _, device in visible_inventory.iterrows():
        status = str(device["Status"]).lower()
        icon = status_icon.get(status, "⚪")
        st.write(f"{icon} {device['Device Name']} - {device['Room']} - {device['Status']}")

with right_col:
    st.write("### Staff Shift Schedule")

    staff_roles = ["All"] + sorted(schedule["Role"].unique().tolist())
    selected_staff_role = st.selectbox("Filter staff by role", staff_roles)

    if selected_staff_role == "All":
        visible_schedule = schedule.copy()
    else:
        visible_schedule = schedule[schedule["Role"] == selected_staff_role]

    st.dataframe(visible_schedule, use_container_width=True)

st.divider()

if role == "Technician":
    st.info("Technician access: view-only access. Device commands are restricted.")

else:
    st.success("Manager access: device command controls are enabled.")

    st.subheader("Device Command Center")

    command_col1, command_col2, command_col3 = st.columns(3)

    with command_col1:
        device_name = st.selectbox("Device", inventory["Device Name"])

    with command_col2:
        command = st.selectbox(
            "Command",
            ["power_on", "power_off", "mute_audio", "unmute_audio", "restart_device"]
        )

    with command_col3:
        staff_member = st.selectbox("Assigned staff", schedule["Employee"])

    device_row = inventory[inventory["Device Name"] == device_name].iloc[0]

    st.write("### Selected Device")
    st.json({
        "device_id": int(device_row["Device ID"]),
        "device_name": device_row["Device Name"],
        "room": device_row["Room"],
        "status": device_row["Status"]
    })

    if st.button("Trigger Device Command"):
        payload = {
            "command": command,
            "device": device_name.lower().replace(" ", "_"),
            "device_id": int(device_row["Device ID"]),
            "room": device_row["Room"],
            "assigned_staff": staff_member,
            "requested_by": role,
            "timestamp": datetime.now().isoformat(),
            "method": "POST",
            "endpoint": "/api/av/device-control"
        }

        st.session_state.command_log.append(payload)

        st.write("### Generated JSON Payload")
        st.json(payload)

        st.write("### Simulated HTTP Request")
        st.code(
            f"""POST /api/av/device-control
Content-Type: application/json

{json.dumps(payload, indent=4)}""",
            language="json"
        )

        st.success("Command generated successfully.")

st.divider()

st.subheader("Command Audit Log")

if len(st.session_state.command_log) == 0:
    st.write("No commands have been triggered yet.")
else:
    st.dataframe(pd.DataFrame(st.session_state.command_log), use_container_width=True)