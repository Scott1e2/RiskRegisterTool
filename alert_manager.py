
# alert_manager.py - Alert Manager for Risk Quantification Tool

import logging
from logging_config import setup_logging
import smtplib
from email.mime.text import MIMEText
import json

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Initialize logging
setup_logging("alert_manager.log")
logger = logging.getLogger(__name__)

# Email settings (example placeholders, replace with actual configurations)
EMAIL_SETTINGS = {
    "smtp_server": "smtp.example.com",
    "port": 587,
    "sender_email": "alerts@example.com",
    "receiver_email": "security_team@example.com",
    "password": "your_password"
}

# Function to send email alerts
def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SETTINGS["sender_email"]
    msg["To"] = EMAIL_SETTINGS["receiver_email"]

    try:
        with smtplib.SMTP(EMAIL_SETTINGS["smtp_server"], EMAIL_SETTINGS["port"]) as server:
            server.starttls()
            server.login(EMAIL_SETTINGS["sender_email"], EMAIL_SETTINGS["password"])
            server.sendmail(EMAIL_SETTINGS["sender_email"], EMAIL_SETTINGS["receiver_email"], msg.as_string())
        logger.info(f"Email alert sent: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")

# Function to generate alerts based on threshold checks
def check_for_alerts(profile_name, risk_score, baseline_drift):
    if risk_score >= config["alert_thresholds"]["critical"]:
        alert_subject = f"Critical Risk Detected for {profile_name}"
        alert_body = f"A critical risk level has been detected for {profile_name}. Risk Score: {risk_score}. Immediate attention is required."
        send_email_alert(alert_subject, alert_body)

    if baseline_drift == "Baseline Drift Detected":
        alert_subject = f"Baseline Drift Detected for {profile_name}"
        alert_body = f"A deviation from the security baseline has been detected for {profile_name}. Review is advised."
        send_email_alert(alert_subject, alert_body)

# Example usage of alert manager with sample inputs
if __name__ == "__main__":
    profile_name = "Vendor A"
    risk_score = 15  # Sample risk score
    baseline_drift = "Baseline Drift Detected"  # Sample drift status

    check_for_alerts(profile_name, risk_score, baseline_drift)
