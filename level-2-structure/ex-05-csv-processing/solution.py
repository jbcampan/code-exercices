import csv
from collections import defaultdict

CSV_INPUT  = "data/instances.csv"
CSV_OUTPUT = "data/filtered.csv"

FIELDNAMES = ["instance_id", "instance_type", "state", "region", "cost_per_hour", "monthly_cost"]


def load_csv(path: str) -> list[dict]:
    """Load a CSV file and return a list of dicts using DictReader."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_running(instances: list[dict]) -> list[dict]:
    """Return only instances whose state is 'running'."""
    return [i for i in instances if i["state"] == "running"]


def add_monthly_cost(instances: list[dict]) -> list[dict]:
    """Add a 'monthly_cost' field (cost_per_hour * 720) to each instance."""
    for instance in instances:
        instance["monthly_cost"] = round(float(instance["cost_per_hour"]) * 720, 2)
    return instances


def export_csv(instances: list[dict], path: str) -> None:
    """Write instances to a CSV file using DictWriter."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(instances)


def generate_summary(instances: list[dict]) -> None:
    """Print total monthly cost per region, sorted descending."""
    totals: dict[str, float] = defaultdict(float)
    for instance in instances:
        totals[instance["region"]] += float(instance["monthly_cost"])

    print("Monthly cost by region (running instances)")
    print("-" * 42)
    for region, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region:<20} ${total:>8.2f}")


if __name__ == "__main__":
    instances = load_csv(CSV_INPUT)

    running   = filter_running(instances)
    with_cost = add_monthly_cost(running)

    export_csv(with_cost, CSV_OUTPUT)
    generate_summary(with_cost)