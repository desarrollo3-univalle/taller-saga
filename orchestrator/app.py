from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Service URLs - Use container names defined in docker-compose
VERIFICATION_URL = "http://verification_service:5001"
TECH_CONFISCATION_URL = "http://tech_confiscation_service:5002"
QUARANTINE_URL = "http://quarantine_service:5003"
LOCATION_ASSIGNMENT_URL = "http://location_assignment_service:5004"
GALACTIC_COMMAND_URL = "http://galactic_command_service:5005"

@app.route('/process-immigration', methods=['POST'])
def process_immigration():
    json_data = request.json
    if not json_data or 'alien_id' not in json_data:
         return jsonify({"message": "Missing 'alien_id' in request body"}), 400
    alien_id = json_data.get('alien_id')
    logging.info(f"Starting immigration process for alien: {alien_id}")

    successful_steps = []
    compensation_data = {} # Store data needed for compensation (like tech_id, log_id)
    error_message = ""

    try:
        # 1. Verify Alien (Tentacle Scan)
        logging.info(f"Orchestrator: Calling Verification Service for {alien_id}")
        res = requests.post(f"{VERIFICATION_URL}/verify", json={"alien_id": alien_id}, timeout=10)
        res.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        logging.info(f"Orchestrator: Verification successful for {alien_id}")
        successful_steps.append("verification")

        # 2. Confiscate Tech (Plasma Weapons)
        logging.info(f"Orchestrator: Calling Tech Confiscation Service for {alien_id}")
        res = requests.post(f"{TECH_CONFISCATION_URL}/confiscate", json={"alien_id": alien_id}, timeout=10)
        res.raise_for_status()
        tech_data = res.json()
        compensation_data['tech_id'] = tech_data.get('tech_id') # Store for potential compensation
        logging.info(f"Orchestrator: Tech confiscation successful for {alien_id}. Tech ID: {compensation_data.get('tech_id')}")
        successful_steps.append("tech_confiscation")

        # 3. Quarantine (Exposure to Earth's Bacteria)
        logging.info(f"Orchestrator: Calling Quarantine Service for {alien_id}")
        res = requests.post(f"{QUARANTINE_URL}/start-quarantine", json={"alien_id": alien_id}, timeout=10)
        res.raise_for_status()
        quarantine_data = res.json()
        compensation_data['log_id'] = quarantine_data.get('log_id') # Store for potential compensation
        logging.info(f"Orchestrator: Quarantine successful for {alien_id}. Log ID: {compensation_data.get('log_id')}")
        successful_steps.append("quarantine")

        # 4. Assign Location (Random Earth City)
        logging.info(f"Orchestrator: Calling Location Assignment Service for {alien_id}")
        res = requests.post(f"{LOCATION_ASSIGNMENT_URL}/assign-city", json={"alien_id": alien_id}, timeout=10)
        res.raise_for_status()
        location_data = res.json()
        compensation_data['city'] = location_data.get('city') # Store for potential compensation
        logging.info(f"Orchestrator: Location assignment successful for {alien_id}. City: {compensation_data.get('city')}")
        successful_steps.append("location_assignment")

        logging.info(f"Immigration process completed successfully for alien: {alien_id}")
        return jsonify({"message": f"Alien {alien_id} immigration process completed. Assigned to {compensation_data.get('city')}."}), 200

    except requests.exceptions.RequestException as e:
        failed_step = successful_steps[-1] if successful_steps else "initialization"
        error_message = f"Network or service error during '{failed_step}' step for alien {alien_id}: {e}"
        logging.error(error_message)
    except Exception as e: # Catch potential raise_for_status() errors or others
        # Determine which step failed based on successful_steps
        failed_step = "unknown"
        if "location_assignment" not in successful_steps and "quarantine" in successful_steps:
            failed_step = "location_assignment"
        elif "quarantine" not in successful_steps and "tech_confiscation" in successful_steps:
            failed_step = "quarantine"
        elif "tech_confiscation" not in successful_steps and "verification" in successful_steps:
            failed_step = "tech_confiscation"
        elif "verification" not in successful_steps:
            failed_step = "verification"

        error_message = f"Error during '{failed_step}' step for alien {alien_id}: {e}"
        logging.error(error_message)

    # If we reach here, an error occurred. Perform compensation.
    logging.warning(f"Starting compensation process for alien: {alien_id} due to error: {error_message}")
    compensation_errors = []

    # Compensate in reverse order
    if "location_assignment" in successful_steps:
        try:
            logging.info(f"Orchestrator: Compensating Location Assignment for {alien_id}")
            requests.post(f"{LOCATION_ASSIGNMENT_URL}/remove-from-city", json={"alien_id": alien_id}, timeout=5)
            # No need to raise for status on compensation, just log failure
        except Exception as comp_e:
            logging.error(f"Compensation failed for Location Assignment for alien {alien_id}: {comp_e}")
            compensation_errors.append("Location Assignment")

    if "quarantine" in successful_steps:
        try:
            logging.info(f"Orchestrator: Compensating Quarantine for {alien_id}")
            requests.post(f"{QUARANTINE_URL}/undo-quarantine-log", json={"alien_id": alien_id}, timeout=5)
        except Exception as comp_e:
            logging.error(f"Compensation failed for Quarantine for alien {alien_id}: {comp_e}")
            compensation_errors.append("Quarantine")

    if "tech_confiscation" in successful_steps:
        try:
            logging.info(f"Orchestrator: Compensating Tech Confiscation for {alien_id}")
            requests.post(f"{TECH_CONFISCATION_URL}/return-tech", json={"alien_id": alien_id}, timeout=5)
        except Exception as comp_e:
            logging.error(f"Compensation failed for Tech Confiscation for alien {alien_id}: {comp_e}")
            compensation_errors.append("Tech Confiscation")

    # Always notify Galactic Command on failure, regardless of verification step success
    try:
        logging.info(f"Orchestrator: Notifying Galactic Command about failure for {alien_id}")
        notification_reason = f"Immigration process failed. Original error: {error_message}. Compensation issues: {', '.join(compensation_errors) if compensation_errors else 'None'}."
        requests.post(f"{GALACTIC_COMMAND_URL}/notify-failure", json={"alien_id": alien_id, "reason": notification_reason}, timeout=5)
    except Exception as comp_e:
        logging.error(f"CRITICAL: Failed to notify Galactic Command for alien {alien_id}: {comp_e}")
        compensation_errors.append("Galactic Command Notification")


    final_message = f"Error in immigration process for {alien_id}. Compensation attempted."
    if compensation_errors:
        final_message += f" Compensation failed for steps: {', '.join(compensation_errors)}."

    return jsonify({"message": final_message, "original_error": error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)