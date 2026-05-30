# Ex-1.2 — Filter and Count Occurrences

**Level:** 1  
**Estimated time:** 1h  
**Track:** Python → Basics

---

## Goal

Parse a list of AWS CloudWatch-style event types and rank them by frequency.
The script implements two counting strategies — a manual dict approach and `collections.Counter` —
then displays results through a shared, reusable ranking function.
Real-world use case: identifying which Lambda errors or EC2 lifecycle events occur most often in a log stream.

---

## Concepts covered

- `dict.get(key, default)` — the fundamental pattern for accumulating counts
- `collections.Counter` — the standard library shortcut and when to prefer it
- `sorted(dict.items(), key=lambda x: x[1], reverse=True)` — sorting a mapping by value
- List comprehension for filtering
- Function design: one reusable display function that doesn't care about its input type
- Module-level constants (`ALL_CAPS`)

---

## Folder structure

```
ex-1.2/
├── solution.py
└── README.md
```

---

## Instructions

The event list is defined as a module-level constant inside the script — no input file.

The script must:

1. Count event occurrences using a plain `dict` (manual approach).
2. Count the same list using `collections.Counter`.
3. Display both rankings through the same `display_ranking` function.
4. Support filtering by a minimum threshold and an optional top-N limit.

---

## Functions to implement

```python
def count_occurrences(items: list) -> dict:
    """Count occurrences of each item using dict.get(key, 0) + 1.

    Args:
        items: A flat list of string event names.

    Returns:
        A dict mapping each unique event to its occurrence count.
    """

def count_with_counter(items: list) -> Counter:
    """Count occurrences using collections.Counter.

    Args:
        items: A flat list of string event names.

    Returns:
        A Counter mapping each unique event to its occurrence count.
    """

def display_ranking(counts: dict, threshold: int = 0, top_n: int = None) -> None:
    """Print events sorted by frequency, descending.

    Args:
        counts:    A dict or Counter mapping event names to occurrence counts.
        threshold: Only display events with count strictly greater than this value.
        top_n:     If set, limit output to the N most frequent events.
    """
```

---

## Constraints

- Two separate functions for the two counting strategies — no inline duplication.
- `display_ranking` must work with both a plain `dict` and a `Counter` without modification.
- No global variables — all data flows through function arguments.
- Module-level constants in `ALL_CAPS`; no values hardcoded inside functions.
- All logic inside functions; a `main()` entry point called under `if __name__ == "__main__"`.

---

## Expected output

```
=== Manual dict — full ranking ===
  LAMBDA_TIMEOUT       4
  EC2_START            3
  RDS_CONNECT          3
  S3_PUT               2
  EC2_STOP             2
  S3_DELETE            1

=== Counter — full ranking ===
  LAMBDA_TIMEOUT       4
  EC2_START            3
  RDS_CONNECT          3
  S3_PUT               2
  EC2_STOP             2
  S3_DELETE            1

=== More than 2 occurrences ===
  LAMBDA_TIMEOUT       4
  EC2_START            3
  RDS_CONNECT          3

=== Top 3 events ===
  LAMBDA_TIMEOUT       4
  EC2_START            3
  RDS_CONNECT          3
```

---

## Key takeaways

1. **`dict.get(key, 0) + 1` is the foundational pattern** — understand it before relying on `Counter`; it appears constantly in real codebases where a full Counter isn't warranted.
2. **`Counter` is a subclass of `dict`** — any function that accepts a `dict` already works with a `Counter`, which is why `display_ranking` needs no special handling.
3. **Sort by value, not key** — `sorted(d.items(), key=lambda x: x[1], reverse=True)` is the idiomatic one-liner; memorise the shape, not just the concept.