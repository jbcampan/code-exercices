# Ex-01 — Log File Parser

**Level:** 1 — Basic logic  
**Estimated time:** 1h  
**Track:** Python / Bash → level-1-fundamentals

---

## Goal

Read a text file line by line, extract structured data, display a clean result.

Real-world use case: parsing server logs, Lambda logs, or exported CloudWatch logs.

---

## Concepts covered

- `open()` and file reading
- `str.strip()`, `str.split(maxsplit=n)`
- Single-responsibility functions
- `if __name__ == "__main__"`
- List comprehensions

---

## Folder structure

```
ex-01-logs-parser/
├── README.md          ← this file
├── data/
│   └── access.log     ← input file (provided)
└── solution.py        ← your solution
```

---

## Instructions

The file `data/access.log` contains lines in this format:

```
DATE TIME LEVEL SERVICE MESSAGE
```

Example:

```
2024-06-01 08:12:11 ERROR payment-service Timeout connecting to payment gateway after 30s
2024-06-01 08:13:45 INFO  api-gateway GET /api/v1/products 200 OK in 142ms
```

Write a `solution.py` script that:

1. Reads `data/access.log` line by line
2. Parses each line into a dict `{date, time, level, service, message}`
3. Filters lines with level `ERROR`
4. Displays each error in the format: `[HH:MM:SS] service → message`

**Extension:** add a `count_by_service(entries)` function that prints the number of errors per service, sorted in descending order.

---

## Functions to implement

```python
def parse_line(line: str) -> dict | None:
    """Returns a dict, or None if the line is malformed."""

def filter_errors(entries: list) -> list:
    """Returns only entries with level ERROR."""

def display(entries: list) -> None:
    """Prints each entry as [HH:MM:SS] service → message."""

def count_by_service(entries: list) -> list:
    """Returns a list of (service, count) tuples sorted by count descending."""
```

---

## Constraints

- No flat code at module level — everything inside functions
- File path as a module-level variable (`LOG_FILE = "data/access.log"`), not hardcoded inside a function
- `if __name__ == "__main__":` block required

---

## Expected output

```
[08:12:11] payment-service → Timeout connecting to payment gateway after 30s
[08:14:55] auth-service → Invalid token signature received from 192.168.1.45
[08:16:08] payment-service → Failed to charge card: insufficient funds for order_id=8821
[08:18:44] api-gateway → Upstream service unavailable, returning 503 to client
[08:20:03] worker-service → Unhandled exception in task processor: NullPointerException at line 88
[08:23:05] auth-service → Database connection lost, retrying in 5s
[08:25:11] payment-service → Duplicate transaction detected for order_id=8830
[08:28:14] worker-service → Disk space below threshold: 91% used on /var/data

payment-service : 3
auth-service : 2
worker-service : 2
api-gateway : 1
```

---

## Key takeaways

**Why `split(maxsplit=4)` and not just `split()`?**

The `MESSAGE` field can contain spaces. A plain `split()` would fragment it into multiple elements. By capping at 4 splits, you always get exactly 5 parts — the 4 fixed fields plus everything else in `parts[4]`.

```python
line = "2024-06-01 08:12:11 ERROR payment-service Timeout after 30s retry"

line.split()           # → 8 elements — message is fragmented
line.split(maxsplit=4) # → 5 elements — message is intact
```

**The core pattern:**

```
read → parse → filter → display
```

Each step in its own function. The `__main__` block orchestrates — it does not process.