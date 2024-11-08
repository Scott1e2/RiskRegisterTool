
# cost_impact_analysis.py - Cost Impact Analysis for Risk Quantification Tool

import json
import logging
from logging_config import setup_logging

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("cost_impact_analysis.log")
logger = logging.getLogger(__name__)

# Estimated costs (example values; can be customized)
COST_ESTIMATES = {
    "data_breach": 50000,  # Cost in case of a data breach (in dollars)
    "compliance_violation": 30000,  # Cost for compliance-related penalties
    "downtime_per_hour": 10000,  # Estimated loss per hour of downtime
    "mitigation_costs": {
        "encryption": 2000,
        "access_control": 1000,
        "multi_factor_authentication": 1500
    }
}

# Calculate potential financial impact based on risk factors
def estimate_financial_impact(risk_factors):
    impact = 0
    if risk_factors["data_sensitivity"] == "critical":
        impact += COST_ESTIMATES["data_breach"]
    if risk_factors["compliance_impact"] == "critical":
        impact += COST_ESTIMATES["compliance_violation"]
    return impact

# Estimate the cost-benefit of implementing mitigations
def estimate_mitigation_cost(mitigation_actions):
    total_cost = sum(COST_ESTIMATES["mitigation_costs"].get(action, 0) for action in mitigation_actions)
    return total_cost

# Update risk register entry with financial impact estimation
def update_register_with_costs(profile_name, risk_factors, mitigation_actions):
    impact_estimate = estimate_financial_impact(risk_factors)
    mitigation_cost = estimate_mitigation_cost(mitigation_actions)
    risk_register_path = f"risk_register_entries/risk_register_{profile_name}.json"
    
    if os.path.exists(risk_register_path):
        with open(risk_register_path, "r") as file:
            register_entry = json.load(file)
        
        register_entry["financial_impact_estimate"] = impact_estimate
        register_entry["mitigation_cost_estimate"] = mitigation_cost
        register_entry["cost_benefit_ratio"] = round(impact_estimate / (mitigation_cost + 1), 2)  # +1 to avoid division by zero
        with open(risk_register_path, "w") as file:
            json.dump(register_entry, file, indent=4)
        logger.info(f"Financial impact and mitigation cost added to {profile_name}")

# Example of running cost impact analysis
if __name__ == "__main__":
    profile_name = "Vendor A"
    risk_factors = {
        "data_sensitivity": "critical",
        "compliance_impact": "critical"
    }
    mitigation_actions = ["encryption", "access_control"]
    
    update_register_with_costs(profile_name, risk_factors, mitigation_actions)
