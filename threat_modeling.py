
# threat_modeling.py - Threat Modeling for Risk Quantification Tool

import json
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("threat_modeling.log")
logger = logging.getLogger(__name__)

# STRIDE Threat Categories
STRIDE_THREATS = {
    "Spoofing": "Threat of impersonation, leading to unauthorized access",
    "Tampering": "Modification of data, potentially compromising integrity",
    "Repudiation": "Actions that cannot be denied, causing non-repudiation risks",
    "Information Disclosure": "Exposure of sensitive information",
    "Denial of Service": "Threat to system availability",
    "Elevation of Privilege": "Access rights escalation"
}

# MITRE ATT&CK Tactics (sample subset)
MITRE_ATTACK_TACTICS = {
    "Initial Access": "Techniques that use access vectors to gain entry",
    "Execution": "Execution of malicious code within systems",
    "Persistence": "Ensuring continued access across reboots",
    "Privilege Escalation": "Gaining elevated permissions for privileged actions",
    "Defense Evasion": "Avoiding detection or blocking defenses",
    "Credential Access": "Stealing account credentials"
}

# Map threats to STRIDE and MITRE ATT&CK
def map_threats_to_frameworks(risk_factors):
    threat_mapping = {}
    for factor, value in risk_factors.items():
        if value == "critical":
            if factor == "access_level":
                threat_mapping["STRIDE"] = STRIDE_THREATS["Elevation of Privilege"]
                threat_mapping["MITRE ATT&CK"] = MITRE_ATTACK_TACTICS["Privilege Escalation"]
            elif factor == "data_sensitivity":
                threat_mapping["STRIDE"] = STRIDE_THREATS["Information Disclosure"]
                threat_mapping["MITRE ATT&CK"] = MITRE_ATTACK_TACTICS["Credential Access"]
        elif value == "high":
            if factor == "access_level":
                threat_mapping["STRIDE"] = STRIDE_THREATS["Tampering"]
                threat_mapping["MITRE ATT&CK"] = MITRE_ATTACK_TACTICS["Persistence"]
    return threat_mapping

# Update risk register entry with threat context
def update_register_with_threats(profile_name, threat_mapping):
    risk_register_path = f"risk_register_entries/risk_register_{profile_name}.json"
    if os.path.exists(risk_register_path):
        with open(risk_register_path, "r") as file:
            register_entry = json.load(file)
        
        register_entry["threat_context"] = threat_mapping
        with open(risk_register_path, "w") as file:
            json.dump(register_entry, file, indent=4)
        logger.info(f"Threat context added to risk register for {profile_name}")

# Example of running threat mapping
if __name__ == "__main__":
    profile_name = "Vendor A"
    risk_factors = {
        "data_sensitivity": "critical",
        "access_level": "high"
    }
    threat_mapping = map_threats_to_frameworks(risk_factors)
    update_register_with_threats(profile_name, threat_mapping)
