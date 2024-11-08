
# questionnaire_interface.py - Security Questionnaire Interface for Risk Quantification Tool

import json
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("questionnaire_interface.log")
logger = logging.getLogger(__name__)

# Sample questionnaire data (could be dynamic in a production setting)
def get_questionnaire_responses():
    responses = {
        "data_sensitivity": "high",
        "access_level": "confidential",
        "compliance_impact": "critical"
    }
    return responses

# Map questionnaire responses to risk factors
def map_responses_to_risk_factors(responses):
    mapped_factors = {}
    for factor, values in config["questionnaire_mappings"].items():
        response_value = responses.get(factor)
        if response_value in values:
            mapped_factors[factor] = response_value
        else:
            logger.warning(f"Unexpected value for {factor}: {response_value}")
    return mapped_factors

# Store mapped factors in a risk register format
def save_to_risk_register(mapped_factors, profile_name):
    risk_register_entry = {
        "profile_name": profile_name,
        "risk_factors": mapped_factors,
        "risk_score": calculate_risk_score(mapped_factors)
    }
    with open(f"risk_register_{profile_name}.json", "w") as register_file:
        json.dump(risk_register_entry, register_file, indent=4)
    logger.info(f"Risk register entry created for {profile_name}")

# Calculate a basic risk score based on mappings (custom scoring logic could be added)
def calculate_risk_score(mapped_factors):
    score = 0
    for factor, value in mapped_factors.items():
        weight = config["risk_factors"].get(factor, 1)
        if value == "high" or value == "critical":
            score += 10 * weight
        elif value == "moderate":
            score += 5 * weight
        elif value == "low":
            score += 2 * weight
    return score

# Run the questionnaire mapping process
def run_questionnaire(profile_name="Vendor A"):
    logger.info(f"Starting questionnaire for {profile_name}")
    responses = get_questionnaire_responses()
    mapped_factors = map_responses_to_risk_factors(responses)
    save_to_risk_register(mapped_factors, profile_name)

if __name__ == "__main__":
    run_questionnaire()
