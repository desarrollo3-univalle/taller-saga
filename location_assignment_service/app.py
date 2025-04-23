from flask import Flask, request, jsonify
import random
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Store assignments (simple in-memory dict: { alien_id: city })
assignments = {}
earth_cities = ["New New York", "Neo-Tokyo", "Londonium", "Paris Prime", "Sector 7G", "Neo-Cali"]

@app.route('/assign-city', methods=['POST'])
def assign_city():
    data = request.json
    alien_id = data.get('alien_id')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    logging.info(f"Assigning city for alien: {alien_id}")
    assigned_city = random.choice(earth_cities)
    assignments[alien_id] = assigned_city
    logging.info(f"Alien {alien_id} assigned to city: {assigned_city}")
    return jsonify({"message": f"Alien {alien_id} assigned to {assigned_city}", "city": assigned_city}), 200

@app.route('/remove-from-city', methods=['POST'])
def remove_from_city():
    data = request.json
    alien_id = data.get('alien_id')
    if not alien_id:
        return jsonify({"message": "Missing alien_id"}), 400

    assigned_city = assignments.pop(alien_id, None)

    if assigned_city:
        logging.warning(f"Compensation: Removing alien {alien_id} from city list ({assigned_city})")
        return jsonify({"message": f"Alien {alien_id} removed from city assignment ({assigned_city})"}), 200
    else:
        logging.warning(f"Compensation: No city assignment found for alien {alien_id}")
        return jsonify({"message": f"No city assignment found for {alien_id}"}), 404

@app.route('/assignments', methods=['GET'])
def get_assignments():
    return jsonify(assignments), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004) # Assign a new port