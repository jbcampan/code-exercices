# Ex-1.5 — Handle Errors Gracefully

**Level:** 1  
**Estimated time:** 1h  
**Track:** Python → level-1-fundamentals

---

## Goal

Read multiple JSON config files (one per environment) and extract a `db_host` field from each. Some files may be missing, malformed, or incomplete — the script must never crash, log a clear error for each failure, and exit with code 1 if more than half the files fail.

---

## Concepts covered

- `try/except` with specific exception types
- `FileNotFoundError`, `ValueError`, `KeyError`, `json.JSONDecodeError`
- `json.JSONDecodeError.msg` and `.lineno` for precise error messages
- `raise` to propagate exceptions from utility functions
- `sys.exit(1)` as a failure signal for CI/CD pipelines
- The "functions raise, main catches" pattern

---

## Folder structure

```
ex-1.5/
├── solution.py
├── README.md
└── data/
    ├── prod.json       # valid, contains db_host
    ├── staging.json    # valid, missing db_host
    ├── dev.json        # malformed JSON
    └── qa.json         # file does not exist
```

---

## Instructions

Each file in `data/` is a JSON config for one environment. The script must:

1. Attempt to load and parse each file with `load_config(path)`.
2. Extract the `db_host` field with `get_db_host(config)`.
3. Print the result or a clear error message for each environment.
4. Count failures — if more than half fail, print a summary and call `sys.exit(1)`.

---

## Functions to implement

```python
def load_config(path: str) -> dict:
    """Open and parse a JSON config file.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file contains invalid JSON.
    """

def get_db_host(config: dict) -> str:
    """Extract the db_host field from a config dict.

    Raises:
        KeyError: if the 'db_host' field is missing.
    """

def process_env(name: str, path: str) -> bool:
    """Load config for one environment and print the result.

    Returns True on success, False on any error.
    """
```

---

## Constraints

- No `try/except` inside `load_config` and `get_db_host` — they raise, that's it.
- Every `except` block must print a useful error message.
- Never use `except Exception` without logging.
- File paths defined as a module-level constant, never hardcoded inside functions.

---

## Expected output

```
[prod    ] db_host → db.prod.company.com
[staging ] ERROR   → 'db_host' key missing from config
[dev     ] ERROR   → Invalid JSON: Expecting ',' delimiter (line 3)
[qa      ] ERROR   → File not found: data/qa.json

Too many failures (3/4). Exiting.
```

---

## Key takeaways

- **Functions raise, the main catches.** Utility functions do one thing and signal problems — they don't decide what to do about them. Only the caller has enough context to make that call.
- **Catch the most specific exception type possible.** `except FileNotFoundError` is always better than `except Exception` — it avoids swallowing unrelated bugs and makes the code self-documenting.
- **`sys.exit(1)` is an interface.** For scripts run by CI/CD pipelines, the exit code *is* the communication. Without it, the pipeline doesn't know something went wrong.