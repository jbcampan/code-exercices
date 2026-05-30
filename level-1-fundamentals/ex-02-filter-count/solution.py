from collections import Counter

EVENTS = [
    "EC2_START", "LAMBDA_TIMEOUT", "EC2_STOP", "RDS_CONNECT",
    "LAMBDA_TIMEOUT", "EC2_START", "LAMBDA_TIMEOUT", "S3_PUT",
    "EC2_START", "RDS_CONNECT", "S3_PUT", "LAMBDA_TIMEOUT",
    "EC2_STOP", "S3_DELETE", "RDS_CONNECT",
]

# def count_occurrences(items: list) -> dict:
#     counts = {}

#     for e in items:
#         if e not in counts:
#             counts[e] = 0

#         counts[e] += 1

#     return counts

def count_occurrences(items: list) -> dict:
    """Count occurrences manually using dict.get(key, default)."""
    counts = {}
    for event in items:
        counts[event] = counts.get(event, 0) + 1
    return counts


def count_with_counter(items: list) -> Counter:
    """Count occurrences using collections.Counter."""
    return Counter(items)

# def display_ranking(counts: dict, threshold: int = 0) -> None:
#     ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
#     for event, count in ranked:
#         if count > threshold:
#             print(f"  {event:<20} {count}")

def display_ranking(counts: dict, threshold: int = 0, top_n: int = None) -> None:
    """Print events sorted by frequency, descending.

    Args:
        counts:    A dict or Counter mapping event names to occurrence counts.
        threshold: Only display events with count strictly greater than this value.
        top_n:     If set, limit output to the N most frequent events.
    """
    ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    ranked = [item for item in ranked if item[1] > threshold]
    if top_n is not None:
        ranked = ranked[:top_n]
    for event, count in ranked:
        print(f"  {event:<20} {count}")


def main() -> None:
    manual_counts = count_occurrences(EVENTS)
    counter_counts = count_with_counter(EVENTS)

    print("=== Manual dict — full ranking ===")
    display_ranking(manual_counts)

    print("\n=== Counter — full ranking ===")
    display_ranking(counter_counts)

    print("\n=== More than 2 occurrences ===")
    display_ranking(manual_counts, threshold=2)

    print("\n=== Top 3 events ===")
    display_ranking(counter_counts, top_n=3)


if __name__ == "__main__":
    main()