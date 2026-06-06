from log_entry import LogEntry


def parse_line(line):
    """Parse a single log line into a LogEntry, or return None if the line is empty."""
    stripped = line.strip()
    if not stripped:
        return None

    parts = stripped.split()
    date = parts[0]
    time = parts[1]
    level = parts[2]
    service = parts[3]
    message = " ".join(parts[4:])

    return LogEntry(
        date=date,
        time=time,
        level=level,
        service=service,
        message=message,
    )