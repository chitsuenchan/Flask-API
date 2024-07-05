# Flask JSON API

This Flask application provides a simple JSON API for managing items stored in a JSON file (`data.json`).

## Endpoints

### GET /items

Returns a list of items filtered by query parameters.

**Query Parameters:**
- `id`: Filters items by ID.
- `name`: Filters items by name.

### PUT /items

Updates an item by ID.

**Request Body:**
```json
{
    "id": 1,
    "name": "Updated Item Name"
}
```

### POST /items

Adds a new item.

**Request Body:**
```json
{
    "id": 4,
    "name": "New Item"
}
```

### DELETE /items/<item_id>

Deletes an item by its ID.

### Error Handling

- 400 Bad Request: Missing parameters in request body.
- 404 Not Found: Item with specified ID does not exist.
- 409 Conflict: Item with specified ID already exists (POST operation).

### Installation and Setup
1. Clone the repository.
2. Install dependencies: pip install -r requirements.txt
3. Run the Flask application: python app.py

### Requirements
- Python 3.x
- Flask
