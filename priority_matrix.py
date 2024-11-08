
# priority_matrix.py - Priority Matrix for Risk Quantification Tool

import json
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("priority_matrix.log")
logger = logging.getLogger(__name__)

# Define priority levels based on severity and urgency
PRIORITY_LEVELS = {
    "Critical-Urgent": "Immediate action required; top priority",
    "Critical-Not Urgent": "High importance, but can be scheduled",
    "High-Urgent": "Important action required soon",
    "High-Not Urgent": "Monitor closely; schedule timely response",
    "Medium-Urgent": "Address soon if resources permit",
    "Medium-Not Urgent": "Low priority, can be scheduled",
    "Low": "Monitor or accept risk as needed"
}

# Assign priority level based on severity and urgency
def assign_priority(severity, urgency):
    priority_key = f"{severity}-{urgency}"
    return PRIORITY_LEVELS.get(priority_key, "Undefined Priority")

# Function to update risk register entry with priority level
def update_priority_in_register(profile_name, severity, urgency):
    priority = assign_priority(severity, urgency)
    risk_register_path = f"risk_register_entries/risk_register_{profile_name}.json"
    
    if os.path.exists(risk_register_path):
        with open(risk_register_path, "r") as file:
            register_entry = json.load(file)
        
        register_entry["priority_level"] = priority
        with open(risk_register_path, "w") as file:
            json.dump(register_entry, file, indent=4)
        logger.info(f"Priority level assigned to {profile_name}: {priority}")

# Example of running priority assignment
if __name__ == "__main__":
    profile_name = "Vendor A"
    severity = "Critical"  # Sample severity
    urgency = "Urgent"  # Sample urgency

    update_priority_in_register(profile_name, severity, urgency)
