import os
import tempfile
import unittest

from ledger import store
from ledger.models import Entry


class StoreTest(unittest.TestCase):
    def test_append_then_load_round_trips(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ledger.json")
            store.append(path, Entry("2026-01-05", 12.5, "food", "lunch"))
            self.assertEqual(store.load(path), [Entry("2026-01-05", 12.5, "food", "lunch")])

    def test_missing_file_is_empty(self):
        self.assertEqual(store.load("/nonexistent/ledger.json"), [])


if __name__ == "__main__":
    unittest.main()
