from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/notify-failure', methods=['POST'])
def notify_failure():
    data = request.json
    alien_id = data.get('alien_id')
    reason = data.get('reason', 'Unknown reason')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    logging.critical(f"GALACTIC COMMAND NOTIFIED: Immigration failure for alien {alien_id}. Reason: {reason}")
    # In a real system, this might send an alert, log to a critical system, etc.
    return jsonify({"message": f"Galactic Command notified about failure for alien {alien_id}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005) # Assign a new port