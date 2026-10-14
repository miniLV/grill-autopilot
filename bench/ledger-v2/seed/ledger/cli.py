import argparse
import sys

from ledger import store
from ledger.models import Entry


def build_parser():
    parser = argparse.ArgumentParser(prog="ledger")
    parser.add_argument("--file", default="ledger.json")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("date")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("note", nargs="?", default="")
    sub.add_parser("list")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "add":
        store.append(args.file, Entry(args.date, float(args.amount), args.category, args.note))
        return 0
    if args.command == "list":
        for e in store.load(args.file):
            print(f"{e.date} {e.amount:.2f} {e.category} {e.note}".rstrip())
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
