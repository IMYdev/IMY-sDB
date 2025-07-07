# IMYDB Class Documentation

## Overview

`IMYDB` is a flexible key-value data store that supports two interchangeable backends:

- **Local JSON file** (with nested key support via dot notation)
- **MongoDB collection** (ideal for shared or cloud-based storage)

Both implementations share the same interface, making it easy to switch between them without changing your code.

---

## Installation

For the MongoDB backend, make sure to install `pymongo`:

```bash
pip install pymongo
```

---

## Environment Setup (MongoDB Only)

Set your MongoDB connection string as an environment variable:

```bash
export MONGO_URL="mongodb://localhost:27017"
```

---

## Initialization

### JSON Backend

```python
db = IMYDB("my_data.json")
```

### MongoDB Backend

```python
# Ensure MONGO_URL is set in your environment
from imysdbMongo import IMYDB  # Use the MongoDB implementation

db = IMYDB("my_data.json")  # file_path acts as the collection name
```

---

## Methods

### `set(key, value)`

Stores a value under the specified key.

- JSON: Supports nested keys via dot notation (e.g., `"user.name"`)
- MongoDB: Keys are treated as flat strings

### `get(key, default=None)`

Returns the value for the given key, or `default` if the key doesn't exist.

### `update(key, value)`

Updates the value only if the key exists.

### `delete(key)`

Deletes the key from storage.

### `exists(key)`

Returns `True` if the key exists, otherwise `False`.

---

## Example Usage

```python
db.set("user.name", "Alice")
print(db.get("user.name"))       # => "Alice"
db.update("user.name", "Alicia")
print(db.exists("user.name"))    # => True
db.delete("user.name")
```

---

## JSON Backend Details

- Stores data in a readable `.json` file
- Supports nested keys via dot notation
- Automatically creates the file and folders if missing

## MongoDB Backend Details

- Requires `MONGO_URL` environment variable
- Uses file path to generate a unique collection name (slashes => underscores)
- Data is stored with `_id` as the key
- No dot-notation nesting

---

## Notes

- The backend implementation is separate; ensure you're using the correct version of the class.
- This code is optimized for my own usage, you might need to change a few things for different use cases.

---

