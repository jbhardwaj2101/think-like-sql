"""Minimal interactive SQLite runner for How SQL Thinks."""
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("practice.sqlite")
if not DB.is_file():
    raise SystemExit("Missing practice.sqlite. Put it beside practice.py.")
connection = sqlite3.connect(DB)
print("How SQL Thinks: enter SQL, end with a semicolon; type quit to exit.")
buffer = ""
while True:
    try:
        line = input("sql> " if not buffer else "...> ")
    except (EOFError, KeyboardInterrupt):
        print()
        break
    if line.strip().lower() in {"quit", "exit"}:
        break
    buffer += line + "\n"
    if not sqlite3.complete_statement(buffer):
        continue
    try:
        cursor = connection.execute(buffer)
        if cursor.description:
            print(" | ".join(column[0] for column in cursor.description))
            for row in cursor.fetchall():
                print(" | ".join("NULL" if v is None else str(v) for v in row))
        else:
            connection.commit()
            print("OK")
    except sqlite3.Error as error:
        print("SQL error:", error)
    buffer = ""
connection.close()
