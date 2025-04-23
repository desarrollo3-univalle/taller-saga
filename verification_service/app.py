from flask import Flask, request, jsonify
import logging # Add logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO) # Add logging

# Store verified aliens (simple in-memory list)
verifications = []

@app.route('/verify', methods=['POST'])
def verify_alien():
    data = request.json
    alien_id = data.get('alien_id')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    # Simulate verification process (e.g., tentacle scan)
    logging.info(f"Attempting verification for alien: {alien_id}")
    # In a real scenario, this would involve more complex logic
    verifications.append(alien_id)
    logging.info(f"Alien {alien_id} verified successfully.")
    return jsonify({"message": f"Alien {alien_id} verified (tentacle scan complete)"}), 200

@app.route('/compensate-verification', methods=['POST'])
def compensate_verification():
    # Compensation for verification might just be logging or an external notification.
    # For this example, we don't remove from the list, as failure implies it wasn't fully processed.
    # The main compensation is notifying Galactic Command, handled by the orchestrator.
    data = request.json
    alien_id = data.get('alien_id')
    logging.warning(f"Compensation requested for verification step for alien: {alien_id}. No data rollback needed here, Galactic Command notified by orchestrator.")
    # If there were specific resources locked during verification, unlock them here.
    return jsonify({"message": f"Verification compensation noted for {alien_id} (handled via Galactic Command notification)"}), 200

@app.route('/verifications', methods=['GET'])
def get_verifications():
    return jsonify(verifications), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) # Keep port or change if needed