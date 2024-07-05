from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)

# Function to load data from JSON file
def load_data():
    data_file = 'data.json'
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    else:
        return []  # Return empty list if file does not exist

@app.route('/items', methods=['GET'])
def get_data():
    data = load_data()

    # Get query parameters
    item_id = request.args.get('id')
    name = request.args.get('name')

    if item_id:
        # Filter data by id if id parameter is provided
        data = [item for item in data if item.get('id') == int(item_id)]

    if name:
        # Filter data by name if name parameter is provided
        data = [item for item in data if item.get('name') == name]

    return jsonify(data)

@app.route('/items', methods=['PUT'])
def update_item():
    request_data = request.get_json()

    # Ensure 'id' is provided in the request data
    if 'id' not in request_data:
        abort(400, "Missing 'id' in request body")

    item_id = request_data['id']

    data = load_data()  # Load current data

    # Find the item by id
    item = next((item for item in data if item['id'] == item_id), None)

    if not item:
        abort(404, f"Item with id {item_id} not found")  # Abort with 404 if item not found

    # Update item's name if provided in request
    if 'name' in request_data:
        item['name'] = request_data['name']

    # Save updated data back to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify(item), 200

@app.route('/items', methods=['POST'])
def add_item():
    request_data = request.get_json()

    # Ensure 'id' and 'name' are provided in the request data
    if 'id' not in request_data or 'name' not in request_data:
        abort(400, "Missing 'id' or 'name' in request body")

    new_item_id = request_data['id']

    data = load_data()  # Load current data

    # Check if an item with the same id already exists
    existing_item = next((item for item in data if item['id'] == new_item_id), None)

    if existing_item:
        abort(409, f"Item with id {new_item_id} already exists")  # Abort with 409 if item already exists

    # If item does not exist, add it to the data
    new_item = {
        'id': new_item_id,
        'name': request_data['name']
    }
    data.append(new_item)

    # Save updated data back to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify(new_item), 201  # Return 201 (Created) status code

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()  # Load current data

    # Find the item by id
    item = next((item for item in data if item['id'] == item_id), None)

    if not item:
        abort(404, f"Item with id {item_id} not found")  # Abort with 404 if item not found

    # Remove the item from data list
    data = [item for item in data if item['id'] != item_id]

    # Save updated data back to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({'message': f'Item with id {item_id} deleted'}), 200

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404

@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': str(error)}), 409

if __name__ == '__main__':
    app.run(debug=True)
