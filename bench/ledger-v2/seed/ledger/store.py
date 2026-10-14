import json
import os

from ledger.models import Entry


def load(path):
    """Return the entries stored at path, or [] if the file does not exist."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [Entry.from_dict(item) for item in data["entries"]]


def save(path, entries):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"entries": [e.to_dict() for e in entries]}, f, indent=2)


def append(path, entry):
    entries = load(path)
    entries.append(entry)
    save(path, entries)
