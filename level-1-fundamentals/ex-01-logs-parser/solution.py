LOG_FILE = "data/access.log"

def parse_line(line: str) -> dict | None:
    parts = line.strip().split(maxsplit=4)

    if len(parts) < 5:
        return None

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "service": parts[3],
        "message": parts[4]
    }


def filter_errors(entries: list) -> list:
    errors = []

    for entry in entries:
        if entry["level"] == "ERROR":
            errors.append(entry)

    return errors


def display(entries: list) -> None:
    for e in entries:
        print(f"[{e['time']}] {e['service']} → {e['message']}")


def count_by_service(entries: list) -> list:
    counts = {}

    # 1. Count errors per service
    for entry in entries:
        service = entry["service"]

        if service not in counts:
            counts[service] = 0

        counts[service] += 1

    # 2. Convert to list of tuples and sort by count (descending)
    sorted_counts = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_counts

if __name__ == "__main__":
    with open(LOG_FILE) as file:
        lines = file.readlines()

    entries = [parse_line(l) for l in lines]
    entries = [e for e in entries if e is not None]
    errors  = filter_errors(entries)
    display(errors)
    counts = count_by_service(errors)
    
    for service, count in counts:
        print(f'{service} : {count}')