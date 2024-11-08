
# dependency_mapper.py - Dependency Mapper for Risk Quantification Tool

import json
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("dependency_mapper.log")
logger = logging.getLogger(__name__)

# Map dependencies for each profile
def map_dependencies(profile_name):
    for profile in config["third_party_profiles"]:
        if profile["name"] == profile_name:
            dependencies = profile.get("dependencies", [])
            logger.info(f"Dependencies mapped for {profile_name}: {dependencies}")
            return dependencies
    logger.warning(f"No dependencies found for {profile_name}")
    return []

# Update risk register entry with dependency mapping
def update_register_with_dependencies(profile_name):
    dependencies = map_dependencies(profile_name)
    risk_register_path = f"risk_register_entries/risk_register_{profile_name}.json"
    
    if os.path.exists(risk_register_path):
        with open(risk_register_path, "r") as file:
            register_entry = json.load(file)
        
        register_entry["dependencies"] = dependencies
        register_entry["dependency_impact"] = prioritize_based_on_dependencies(dependencies)
        with open(risk_register_path, "w") as file:
            json.dump(register_entry, file, indent=4)
        logger.info(f"Dependency impact updated for {profile_name}")

# Prioritize risks based on criticality of dependencies
def prioritize_based_on_dependencies(dependencies):
    # Example scoring: critical dependencies increase impact score
    impact_score = len(dependencies) * 5  # Basic scoring for demonstration
    return impact_score

# Example usage
if __name__ == "__main__":
    profile_name = "Vendor A"
    update_register_with_dependencies(profile_name)
