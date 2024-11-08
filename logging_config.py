
# logging_config.py - Centralized Logging Setup for Risk Quantification Tool

import logging

# Configure logging settings
def setup_logging(log_file="risk_quantification_tool.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete.")
