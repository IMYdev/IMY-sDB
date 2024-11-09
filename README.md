# IMYDB Class Documentation

## Overview
The `IMYDB` class provides a simple way to manage data in a JSON file. It supports basic operations such as setting, getting, updating, and deleting data using dot notation for nested keys.

## Class Initialization

### `__init__(self, file_path)`
- **Parameters:**
  - `file_path` (str): Path to the JSON file where data will be stored.
  
- **Description:** Initializes the class and loads data from the file, creating the file if it doesn't exist.

---

## Methods

### `load_data(self)`
- **Description:** Loads data from the JSON file. If the file doesn't exist or is invalid, it initializes with an empty dictionary.

### `save_data(self)`
- **Description:** Saves the current data to the JSON file.

---

### `set(self, key, value)`
- **Parameters:**
  - `key` (str): The key (supports dot notation for nested keys).
  - `value` (any): The value to set.

- **Description:** Sets the value for the specified key and saves the data.

---

### `get(self, key, default=None)`
- **Parameters:**
  - `key` (str): The key to get (supports dot notation for nested keys).
  - `default` (any, optional): The value to return if the key doesn't exist.

- **Description:** Retrieves the value associated with the key, or returns `default` if the key doesn't exist.

---

### `delete(self, key)`
- **Parameters:**
  - `key` (str): The key to delete (supports dot notation for nested keys).

- **Description:** Deletes the key from the data and saves the changes.

---

### `update(self, key, value)`
- **Parameters:**
  - `key` (str): The key to update.
  - `value` (any): The new value.

- **Description:** Updates the value of an existing key. Does nothing if the key doesn't exist.

---

### `exists(self, key)`
- **Parameters:**
  - `key` (str): The key to check for existence.

- **Description:** Returns `True` if the key exists, otherwise `False`.

---

## Helper Methods

### `_set_nested(self, data, keys, value)`
- **Description:** Helper method to set a value in a nested dictionary using a list of keys.

---

### `_get_nested(self, data, keys, default=None)`
- **Description:** Helper method to retrieve a value from a nested dictionary using a list of keys.

---

### `_delete_nested(self, data, keys)`
- **Description:** Helper method to delete a key from a nested dictionary using a list of keys.

---

## Example Usage

```python
db = IMYDB("my_data.json")

# Setting values
db.set("user.name", "Alice")
db.set("user.age", 25)

# Getting values
name = db.get("user.name", "Unknown")  # Returns 'Alice'
age = db.get("user.age", 0)            # Returns 25

# Checking existence
exists = db.exists("user.name")        # Returns True

# Updating values
db.update("user.age", 26)

# Deleting a key
db.delete("user.name")
