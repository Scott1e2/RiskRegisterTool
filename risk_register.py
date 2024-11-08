
# risk_register.py - Risk Register Manager for Risk Quantification Tool

import json
import os
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("risk_register.log")
logger = logging.getLogger(__name__)

# Path for storing risk register entries
RISK_REGISTER_PATH = "risk_register_entries"

# Initialize directory for risk register entries
if not os.path.exists(RISK_REGISTER_PATH):
    os.makedirs(RISK_REGISTER_PATH)

# Function to update an existing entry or create a new one
def update_risk_register(profile_name, risk_factors, risk_score):
    entry_path = os.path.join(RISK_REGISTER_PATH, f"risk_register_{profile_name}.json")
    entry = {
        "profile_name": profile_name,
        "risk_factors": risk_factors,
        "risk_score": risk_score,
        "baseline_status": assess_baseline_drift(risk_score, profile_name)
    }
    with open(entry_path, "w") as file:
        json.dump(entry, file, indent=4)
    logger.info(f"Risk register entry updated for {profile_name}")

# Function to calculate if the current score is within baseline
def assess_baseline_drift(risk_score, profile_name):
    for profile in config["third_party_profiles"]:
        if profile["name"] == profile_name:
            baseline = profile["baseline"]
            baseline_threshold = config["baseline_tracking"]["baseline_threshold"]
            drift = abs(risk_score - baseline_threshold)
            if drift > baseline_threshold:
                logger.warning(f"Baseline drift detected for {profile_name}")
                return "Baseline Drift"
            return "Within Baseline"
    return "Profile Not Found"

# Function to retrieve all entries for a review
def retrieve_risk_register():
    register_data = []
    for entry_file in os.listdir(RISK_REGISTER_PATH):
        with open(os.path.join(RISK_REGISTER_PATH, entry_file), "r") as file:
            register_data.append(json.load(file))
    return register_data

# Example of updating and retrieving the risk register
if __name__ == "__main__":
    # Example profile to update
    profile_name = "Vendor A"
    risk_factors = {
        "data_sensitivity": "high",
        "access_level": "confidential",
        "compliance_impact": "critical"
    }
    risk_score = 25  # Sample score calculated externally or with questionnaire responses

    # Update the register and then retrieve all entries
    update_risk_register(profile_name, risk_factors, risk_score)
    all_entries = retrieve_risk_register()
    for entry in all_entries:
        print(entry)
