# Ex-2.2 — First Python Class

**Level:** 2
**Estimated time:** 1h30
**Track:** Python → oop-basics

---

## Goal

Model parsed log entries as objects instead of plain dictionaries. `LogEntry` represents a single line of log data with behaviour (type-checking, formatting), while `LogReport` aggregates a list of entries and exposes statistics. This mirrors a real-world pattern where business objects carry both data and the logic that belongs to them.

---

## Concepts covered

- `class`, `__init__`, instance attributes
- Instance methods (`is_error`, `is_warning`, `format_short`, `summary`, …)
- `__repr__` vs `__str__` — debug representation vs user-facing display
- Single-responsibility principle applied to classes
- Standalone parsing function kept outside the model classes
- `json.dump()` for serialisable export

---

## Folder structure

```
ex-2.2/
├── data/
│   └── access.log
├── log_entry.py
├── log_parser.py
├── log_report.py
├── main.py
└── README.md
```

---

## Instructions

**Input file format** — each line in `data/access.log` follows this pattern:

```
YYYY-MM-DD HH:MM:SS LEVEL SERVICE message words...
```

Example:
```
2024-03-15 08:02:16 ERROR auth-service JWT signature verification failed for token=eyJ...
```

**What the script must do:**

1. Read `data/access.log` line by line, skipping empty lines.
2. Parse each line with `parse_line()` (from `log_parser.py`) into a `LogEntry`.
3. Build a `LogReport` from the list of entries.
4. Print a summary (total, error count, warning count, counts by service).
5. Print all error entries.
6. Export the report as `report.json` using `LogReport.to_dict()`.

---

## Functions to implement

```python
# log_entry.py
class LogEntry:
    def __init__(self, date: str, time: str, level: str, service: str, message: str):
        """Store the five fields of a parsed log line."""

    def is_error(self) -> bool:
        """Return True if the log level is ERROR."""

    def is_warning(self) -> bool:
        """Return True if the log level is WARNING."""

    def format_short(self) -> str:
        """Return a compact string: [LEVEL] service: message."""

    def __str__(self) -> str:
        """User-facing display — delegates to format_short()."""

    def __repr__(self) -> str:
        """Debug representation showing all fields except message."""


# log_parser.py
def parse_line(line: str) -> LogEntry | None:
    """
    Split a raw log line into its five components and return a LogEntry.
    Return None if the line is empty or blank.
    LogEntry receives already-parsed data — no parsing logic inside the class.
    """


# log_report.py
class LogReport:
    def __init__(self, entries: list[LogEntry]):
        """Receive a pre-built list of LogEntry objects. No file I/O here."""

    def errors(self) -> list[LogEntry]:
        """Return all entries whose level is ERROR."""

    def warnings(self) -> list[LogEntry]:
        """Return all entries whose level is WARNING."""

    def count_by_service(self) -> dict[str, int]:
        """Return a dict mapping each service name to its total entry count."""

    def summary(self) -> dict:
        """Return a dict with total_logs, errors, warnings, and by_service."""

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict (delegates to summary())."""
```

---

## Constraints

- `LogEntry.__init__` receives already-parsed fields — no string splitting inside the class.
- `LogReport.__init__` receives a list of `LogEntry` — no file reading inside the class.
- All file parsing lives in the standalone `parse_line()` function in `log_parser.py`.
- No instance attribute is modified from outside the class directly.
- The log file path is defined as a module-level constant in `main.py`, never hard-coded inside a function.
- No code executes at module level — only function and class definitions, plus a `__main__` guard.

---

## Expected output

```
=== SUMMARY ===
Total logs : 30
Errors     : 5
Warnings   : 7

Logs by service:
  - api-gateway: 8
  - auth-service: 8
  - storage-service: 7
  - db-service: 7

=== ERRORS ===
[ERROR] auth-service: JWT signature verification failed for token=eyJ...
[ERROR] db-service: Connection pool exhausted: max_connections=20 reached
[ERROR] storage-service: Failed to delete object s3://my-bucket/tmp/stale.log: AccessDenied
[ERROR] api-gateway: Upstream timeout after 30s: service=report-generator
[ERROR] db-service: Deadlock detected between transactions tx=7821 and tx=7822
[ERROR] auth-service: OAuth callback received invalid state parameter — possible CSRF attempt

Report exported to report.json
```

---

## Key takeaways

1. **`__repr__` is for developers, `__str__` is for users.** `repr()` should let you reconstruct or identify the object (used in the REPL, logs, debuggers); `str()` should produce readable output for end users. When in doubt: `__repr__` always, `__str__` only when the display differs.

2. **A class earns its keep when data and behaviour travel together.** A plain dict can hold `{"level": "ERROR"}`, but it can't answer `is_error()`. The moment you find yourself writing `if entry["level"] == "ERROR"` in three different places, a class with a method pays off.

3. **Single responsibility keeps classes small and testable.** `LogEntry` knows what it *is*; `LogReport` knows how to *aggregate*; `parse_line()` knows how to *read*. None of them does the others' job — which means each can be tested and replaced independently.