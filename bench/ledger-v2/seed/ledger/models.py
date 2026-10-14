from dataclasses import dataclass


@dataclass
class Entry:
    date: str  # ISO date, YYYY-MM-DD
    amount: float
    category: str
    note: str = ""

    def to_dict(self):
        return {"date": self.date, "amount": self.amount, "category": self.category, "note": self.note}

    @classmethod
    def from_dict(cls, data):
        return cls(data["date"], data["amount"], data["category"], data.get("note", ""))
