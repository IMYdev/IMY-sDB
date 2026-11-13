import json
import os
import tempfile
from pathlib import Path
from typing import Any


_MISSING = object()


class IMYDB:
    """A lightweight JSON-based key-value database with nested keys."""

    def __init__(self, file_path: str | os.PathLike):
        self.file_path = Path(file_path)
        self.data: dict[str, Any] = {}
        self.load_data()

    def load_data(self) -> None:
        """Load the database, creating it if it doesn't exist."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            self.save_data()
            return
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in database file: {self.file_path}"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError("Database root must be a JSON object.")

        self.data = data

    def save_data(self) -> None:
        """Atomically save the database to disk."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.file_path.parent,
                prefix=f".{self.file_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as file:
                temp_path = Path(file.name)

                json.dump(self.data, file, indent=4, ensure_ascii=False)
                file.write("\n")
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self.file_path)

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()

    @staticmethod
    def _split_key(key: str) -> list[str]:
        """Validate and split a dotted key."""
        if not isinstance(key, str) or not key:
            raise ValueError("Key must be a non-empty string.")

        parts = key.split(".")

        if any(not part for part in parts):
            raise ValueError(f"Invalid nested key: {key!r}")

        return parts

    @staticmethod
    def _get_nested(
        data: dict,
        keys: list[str],
        default: Any = None,
    ) -> Any:
        """Retrieve a value from a nested dictionary."""
        current = data

        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default

            current = current[key]

        return current

    @staticmethod
    def _set_nested(
        data: dict,
        keys: list[str],
        value: Any,
    ) -> None:
        """Set a value inside a nested dictionary."""
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}

            if not isinstance(current[key], dict):
                raise TypeError(
                    f"Cannot traverse '{key}': expected a dictionary."
                )

            current = current[key]

        current[keys[-1]] = value

    @staticmethod
    def _delete_nested(data: dict, keys: list[str]) -> bool:
        """Delete a nested value. Returns whether it existed."""
        current = data

        for key in keys[:-1]:
            if not isinstance(current, dict) or key not in current:
                return False

            current = current[key]

        if not isinstance(current, dict):
            return False

        return current.pop(keys[-1], _MISSING) is not _MISSING

    def set(self, key: str, value: Any) -> None:
        """Set or create a key-value pair."""
        keys = self._split_key(key)
        self._set_nested(self.data, keys, value)
        self.save_data()

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value, returning default when the key is missing."""
        keys = self._split_key(key)
        return self._get_nested(self.data, keys, default)

    def exists(self, key: str) -> bool:
        """Check whether a key exists, even if its value is None."""
        keys = self._split_key(key)
        return self._get_nested(self.data, keys, _MISSING) is not _MISSING

    def delete(self, key: str) -> bool:
        """Delete a key. Returns whether anything was deleted."""
        keys = self._split_key(key)

        if not self._delete_nested(self.data, keys):
            return False

        self.save_data()
        return True

    def update(self, key: str, value: Any) -> bool:
        """Update an existing key without creating a new one."""
        if not self.exists(key):
            return False

        self.set(key, value)
        return True
