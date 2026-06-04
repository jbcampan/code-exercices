"""
Alternative report: error breakdown by hour of day.
Demonstrates that log_parser can be reused to build a different view.
"""
from log_parser import LOG_FILE, parse_line, filter_errors

if __name__ == "__main__":
    with open(LOG_FILE) as f:
        lines = f.readlines()

    entries = [parse_line(line) for line in lines]
    entries = [e for e in entries if e is not None]
    errors = filter_errors(entries)

    # Aggregate by hour (HH extracted from HH:MM:SS)
    by_hour: dict[str, int] = {}
    for error in errors:
        hour = error["time"].split(":")[0]
        by_hour[hour] = by_hour.get(hour, 0) + 1

    print("=== Errors by hour ===")
    for hour in sorted(by_hour):
        bar = "█" * by_hour[hour]
        print(f"  {hour}h  {bar}  ({by_hour[hour]})")