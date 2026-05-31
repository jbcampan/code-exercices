# Ex-1.3 — Parse a JSON Response and Extract Fields

**Level:** 1  
**Estimated time:** 1h  
**Track:** Python → basics

---

## Goal

Read a JSON file that simulates a real AWS `describe_instances` response, navigate its nested structure safely, and print a formatted table of instances. The real-world use case is parsing any boto3 response — virtually every AWS SDK call returns deeply nested dicts where fields can be missing.

---

## Concepts covered

- `json.load()` to deserialize a JSON file
- Safe nested navigation with `.get()` and the `dict.get("key", {}).get("subkey", "N/A")` pattern
- Iterating over `Reservations → Instances` (the real EC2 API structure)
- Extracting values from a list of `{"Key": ..., "Value": ...}` tag dicts
- f-string column alignment with `:<N`
- Optional filtering via a default-`None` parameter

---

## Folder structure

```
ex-1.3/
├── data/
│   └── instances.json
├── solution.py
└── README.md
```

---

## Instructions

`data/instances.json` simulates a `describe_instances` response with two reservations:

- One instance that is **running**, has a `Name` tag, and has a public IP.
- One instance that is **stopped**, has no `Name` tag, and has no public IP.

The script must:

1. Load the JSON file.
2. Iterate over every `Reservation` and every `Instance` within it.
3. For each instance, extract: `InstanceId`, `InstanceType`, state name, public IP, and the `Name` tag.
4. Optionally filter by state when `state_filter` is provided.
5. Print a aligned table with a header and separator line.

---

## Functions to implement

```python
def load_json(path: str) -> dict:
    """Load and return the JSON file at *path* as a dict."""

def get_tag(tags: list, key: str) -> str:
    """Return the Value for *key* in a list of {'Key':..,'Value':..} dicts.

    Returns 'N/A' if the key is absent or *tags* is empty / None.
    Must never raise, regardless of input.
    """

def extract_instances(data: dict, state_filter: str = None) -> list:
    """Return a list of dicts, one per instance, with keys:
    id, type, state, ip, name.

    If *state_filter* is given, only include instances whose state matches.
    Handles an empty or missing 'Reservations' key without raising.
    """

def display(instances: list) -> None:
    """Print a formatted table of instances with aligned columns."""
```

---

## Constraints

- `get_tag` must never raise, regardless of what is passed in.
- `extract_instances` must handle an empty `Reservations` list without raising.
- No direct key access (`data["key"]`) anywhere — always use `.get()`.
- File path defined as a module-level constant, not hard-coded inside functions.
- No code executed at module level outside of functions and the `__main__` block.

---

## Expected output

```
InstanceId             Type         State      IP               Name
----------------------------------------------------------------------
i-0a1b2c3d4e5f67890   t3.micro     running    54.210.101.22    web-server-01
i-0b2c3d4e5f6789012   t3.small     stopped    N/A              N/A
```

---

## Key takeaways

1. **Always use `.get()` on API responses.** Real AWS responses omit fields constantly — a direct `data["key"]` will crash in production sooner or later.
2. **The `Reservations → Instances` nesting is real.** Every `describe_instances` call wraps results this way; knowing the structure saves you from confusion when working with boto3.
3. **Default-`None` parameters for optional filters** keep function signatures clean and backward-compatible — callers who don't need filtering don't need to change anything.