from log_parser import LOG_FILE, parse_line, filter_errors, count_by_service, format_entries, to_csv

CSV_OUTPUT = "data/errors.csv"

if __name__ == "__main__":
    with open(LOG_FILE) as f:
        lines = f.readlines()

    entries = [parse_line(line) for line in lines]
    entries = [e for e in entries if e is not None]
    errors = filter_errors(entries)

    print("=== Error log ===")
    for line in format_entries(errors):
        print(line)

    print("\n=== Errors by service ===")
    for service, count in count_by_service(errors):
        print(f"  {service}: {count}")

    to_csv(errors, CSV_OUTPUT)
    print(f"\nExported {len(errors)} errors to {CSV_OUTPUT}")