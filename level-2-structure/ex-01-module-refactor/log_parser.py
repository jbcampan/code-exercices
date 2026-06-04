import csv

__all__ = [
    "LOG_FILE",
    "parse_line",
    "filter_errors",
    "count_by_service",
    "format_entries",
    "to_csv",
]

LOG_FILE = "data/access.log"


def parse_line(line: str) -> dict | None:
    """Parse a single log line into a dict, or return None if malformed."""
    parts = line.strip().split(maxsplit=4)

    if len(parts) < 5:
        return None

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4],
    }


def filter_errors(entries: list) -> list:
    """Return only entries whose level is ERROR."""
    return [e for e in entries if e["level"] == "ERROR"]


def count_by_service(entries: list) -> list[tuple[str, int]]:
    """Return a list of (service, count) tuples sorted by count descending."""
    counts = {}

    for entry in entries:
        service = entry["service"]
        counts[service] = counts.get(service, 0) + 1

    return sorted(counts.items(), key=lambda item: item[1], reverse=True)


def format_entries(entries: list) -> list[str]:
    """Return a list of human-readable strings for the given entries."""
    return [f"[{e['time']}] {e['service']} → {e['message']}" for e in entries]


def to_csv(entries: list, path: str) -> None:
    """Export a list of log entry dicts to a CSV file at the given path."""
    if not entries:
        return

    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=entries[0].keys())
        writer.writeheader()
        writer.writerows(entries)