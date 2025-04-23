from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Store quarantine logs (simple in-memory dict: { alien_id: log_id })
quarantine_logs = {}
log_counter = 0

@app.route('/start-quarantine', methods=['POST'])
def start_quarantine():
    global log_counter
    data = request.json
    alien_id = data.get('alien_id')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    logging.info(f"Starting quarantine process for alien: {alien_id}")
    # Simulate quarantine process (exposure to bacteria)
    log_id = f"qlog_{log_counter}"
    log_counter += 1
    quarantine_logs[alien_id] = log_id
    logging.info(f"Alien {alien_id} quarantine started. Log ID: {log_id}")
    return jsonify({"message": f"Quarantine cleared for {alien_id}", "log_id": log_id}), 200

@app.route('/undo-quarantine-log', methods=['POST'])
def undo_quarantine_log():
    data = request.json
    alien_id = data.get('alien_id')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    log_id = quarantine_logs.pop(alien_id, None) # Remove and get value, default None

    if log_id:
        logging.warning(f"Compensation: Undoing quarantine log {log_id} for alien {alien_id}")
        return jsonify({"message": f"Quarantine log {log_id} undone for {alien_id}"}), 200
    else:
        logging.warning(f"Compensation: No quarantine log found for alien {alien_id}")
        return jsonify({"message": f"No quarantine log found for {alien_id}"}), 404

@app.route('/quarantine-logs', methods=['GET'])
def get_quarantine_logs():
    return jsonify(quarantine_logs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003) # Keep port or change if needed