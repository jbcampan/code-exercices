import json
import sys

CONFIGS = {
    "prod":    "data/prod.json",
    "staging": "data/staging.json",
    "dev":     "data/dev.json",
    "qa":      "data/qa.json",
}


def load_config(path: str) -> dict:
    """Open and parse a JSON config file.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file contains invalid JSON.
    """
    with open(path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e.msg} (line {e.lineno})")


def get_db_host(config: dict) -> str:
    """Extract the db_host field from a config dict.

    Raises:
        KeyError: if the field is missing.
    """
    if "db_host" not in config:
        raise KeyError("'db_host' key missing from config")
    return config["db_host"]


def process_env(name: str, path: str) -> bool:
    """Load config for one environment and print the result.

    Returns True on success, False on any error.
    """
    try:
        config = load_config(path)
        host = get_db_host(config)
        print(f"[{name:<8}] db_host → {host}")
        return True
    except FileNotFoundError:
        print(f"[{name:<8}] ERROR   → File not found: {path}")
    except ValueError as e:
        print(f"[{name:<8}] ERROR   → {e}")
    except KeyError as e:
        msg = e.args[0]
        print(f"[{name:<8}] ERROR   → {msg}")
    return False


if __name__ == "__main__":
    results = [process_env(name, path) for name, path in CONFIGS.items()]

    failures = results.count(False)
    if failures > len(results) / 2:
        print(f"\nToo many failures ({failures}/{len(results)}). Exiting.")
        sys.exit(1)