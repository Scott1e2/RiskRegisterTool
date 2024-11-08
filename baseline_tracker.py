
# baseline_tracker.py - Baseline Tracker for Risk Quantification Tool

import os
import json
import logging
from logging_config import setup_logging
from continuous_monitoring_interface import check_monitoring_tool

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("baseline_tracker.log")
logger = logging.getLogger(__name__)

# Function to update baseline entries with continuous monitoring insights
def update_baseline_with_monitoring(profile_name):
    monitoring_findings = check_monitoring_tool(profile_name)
    risk_register_path = f"risk_register_entries/risk_register_{profile_name}.json"

    if os.path.exists(risk_register_path):
        with open(risk_register_path, "r") as file:
            register_entry = json.load(file)

        # Adjust baseline based on continuous monitoring findings
        register_entry["continuous_monitoring_findings"] = monitoring_findings
        baseline_drift = assess_baseline_drift(register_entry["risk_score"], monitoring_findings)

        register_entry["baseline_drift_status"] = baseline_drift
        with open(risk_register_path, "w") as file:
            json.dump(register_entry, file, indent=4)
        logger.info(f"Baseline updated with monitoring data for {profile_name}")

# Assess if the monitoring findings indicate a baseline drift
def assess_baseline_drift(risk_score, monitoring_findings):
    baseline_threshold = config["baseline_tracking"]["baseline_threshold"]
    adjusted_score = risk_score + sum(monitoring_findings.values())
    drift = abs(adjusted_score - baseline_threshold)

    if drift > baseline_threshold:
        logger.warning("Baseline drift detected based on continuous monitoring data")
        return "Baseline Drift Detected"
    return "Within Baseline"

# Run baseline tracker process
def run_baseline_tracker(profile_name="Vendor A"):
    logger.info("Starting baseline tracking with continuous monitoring integration")
    update_baseline_with_monitoring(profile_name)

if __name__ == "__main__":
    run_baseline_tracker()
