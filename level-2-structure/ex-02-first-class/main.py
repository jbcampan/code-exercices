import json

from log_parser import parse_line
from log_report import LogReport

LOG_FILE = "data/access.log"
OUTPUT_FILE = "report.json"


def load_entries(path):
    entries = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            entry = parse_line(line)
            if entry is not None:
                entries.append(entry)
    return entries


def main():
    entries = load_entries(LOG_FILE)
    report = LogReport(entries)
    summary = report.summary()

    print("=== SUMMARY ===")
    print(f"Total logs : {summary['total_logs']}")
    print(f"Errors     : {summary['errors']}")
    print(f"Warnings   : {summary['warnings']}")

    print("\nLogs by service:")
    for service, count in summary["by_service"].items():
        print(f"  - {service}: {count}")

    print("\n=== ERRORS ===")
    for error in report.errors():
        print(error)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2)
    print(f"\nReport exported to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()