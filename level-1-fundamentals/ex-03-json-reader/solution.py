import json

DATA_PATH = "data/instances.json"


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def get_tag(tags: list, key: str) -> str:
    for tag in tags:
        if tag.get("Key") == key:
            return tag.get("Value", "N/A")
    return "N/A"


def extract_instances(data: dict, state_filter: str = None) -> list:
    result = []
    for reservation in data.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            state = instance.get("State", {}).get("Name", "N/A")
            if state_filter is not None and state != state_filter:
                continue
            result.append({
                "id":    instance.get("InstanceId", "N/A"),
                "type":  instance.get("InstanceType", "N/A"),
                "state": state,
                "ip":    instance.get("PublicIpAddress", "N/A"),
                "name":  get_tag(instance.get("Tags", []), "Name"),
            })
    return result


def display(instances: list) -> None:
    print(f"{'InstanceId':<22} {'Type':<12} {'State':<10} {'IP':<16} {'Name'}")
    print("-" * 70)
    for i in instances:
        print(f"{i['id']:<22} {i['type']:<12} {i['state']:<10} {i['ip']:<16} {i['name']}")


if __name__ == "__main__":
    data = load_json(DATA_PATH)
    instances = extract_instances(data)
    display(instances)