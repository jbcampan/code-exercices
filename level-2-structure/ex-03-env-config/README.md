# Ex-2.3 — Configuration with `os.environ`

**Level:** 2  
**Estimated time:** 1h  
**Track:** Python → environment-and-config

---

## Goal

A script that simulates a database connection tool whose parameters are driven
entirely by environment variables. This mirrors how real services are configured
in Docker containers, AWS Lambda functions, and CI/CD pipelines — where a single
codebase must behave differently across dev, staging, and production without any
code change.

---

## Concepts covered

- `os.environ.get(key, default)` vs `os.environ[key]` — and when each is appropriate
- `os.getenv()` as a shorthand alias
- Manual `.env` file parsing (line by line, no third-party library)
- Injecting values into `os.environ` before reading them
- Config validation at startup with `ValueError`
- Separating config loading from the rest of the business logic
- The `.env` / `.env.example` convention

---

## Folder structure

```
ex-2.3/
├── solution.py
├── .env.example
├── .gitignore
└── README.md
```

---

## Instructions

**Input:** environment variables (from the shell or a `.env` file).

The script must:

1. Parse `.env` if the file exists, injecting each `KEY=value` pair into
   `os.environ` — only for keys that are not already set.
2. Read the four variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `LOG_LEVEL`) and
   return them as a typed dict.
3. Validate that every required variable is present and non-empty; stop
   immediately with a clear error message if not.
4. Simulate a database connection by printing the active configuration.

---

## Functions to implement

```python
def load_env_file(path: str = ".env") -> None:
    """Read a .env file and inject variables into os.environ.

    - Skip blank lines and lines starting with '#'.
    - Only inject keys that are not already set in os.environ
      (shell always wins over .env file).
    - Does nothing if the file does not exist.
    """

def load_config() -> dict:
    """Load configuration exclusively from os.environ.

    Calls load_env_file() first, then reads:
      - DB_HOST    (required, no default)
      - DB_PORT    (optional, default 5432, must be castable to int)
      - DB_NAME    (required, no default)
      - LOG_LEVEL  (optional, default "INFO")

    Returns a clean dict with typed values.
    This is the ONLY function allowed to read os.environ.
    """

def validate_config(config: dict) -> None:
    """Raise ValueError if any required key is missing or empty.

    Required keys: db_host, db_name.
    Report all missing keys in a single error message.
    """

def connect(config: dict) -> None:
    """Simulate a database connection using the provided config dict."""
```

---

## Constraints

- `load_config()` is the **only** function that reads `os.environ`; all other
  functions receive config as a parameter.
- Validation runs **before** any action — if a variable is missing, the script
  exits immediately with a human-readable error.
- No hardcoded values outside of `load_config()`.
- `.env` is listed in `.gitignore`; `.env.example` is committed to the repo.
- `.env` parsing must be done manually — no `python-dotenv` or similar library.

---

## Expected output

```
# With DB_HOST=localhost DB_NAME=mydb python solution.py
[INFO] Connecting to database...
  Host : localhost:5432
  DB   : mydb

Active configuration:
{
  "db_host": "localhost",
  "db_port": 5432,
  "db_name": "mydb",
  "log_level": "INFO"
}

# With DB_HOST=localhost python solution.py  (DB_NAME missing)
[ERROR] Configuration error: Missing required configuration: db_name
```

---

## Key takeaways

1. **`os.environ.get(key)` vs `os.environ[key]`** — `.get()` returns `None`
   silently; direct key access raises `KeyError`. For required variables, the
   explicit error from `KeyError` is arguably more honest — but a custom
   `ValueError` with a clear message is better still.

2. **Validate at startup, not at use** — if you check for `DB_HOST` only when
   the connection is attempted, a missing variable surfaces deep in the call
   stack, possibly after side effects. Validating upfront makes failures fast,
   loud, and easy to diagnose.

3. **Shell always wins over `.env`** — the convention (`if key not in
   os.environ`) lets operators override any file-based default without editing
   files, which is the expected behaviour in Docker and CI environments.