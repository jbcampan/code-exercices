import os
import json

ENV_FILE = ".env"


def load_env_file(path: str = ENV_FILE) -> None:
    """Read a .env file and inject variables into os.environ (if not already set)."""
    if not os.path.isfile(path):
        return

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key and key not in os.environ:
                os.environ[key] = value


def load_config() -> dict:
    """Load configuration from environment variables.

    Reads .env file first (if present), then os.environ.
    Returns a clean config dict — this is the only function that touches os.environ.
    """
    load_env_file()

    raw_port = os.getenv("DB_PORT", "5432")
    try:
        db_port = int(raw_port)
    except ValueError:
        raise ValueError(
            f"DB_PORT must be an integer, got: {raw_port!r}"
        )

    return {
        "db_host": os.environ.get("DB_HOST"),
        "db_port": db_port,
        "db_name": os.environ.get("DB_NAME"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }


def validate_config(config: dict) -> None:
    """Raise ValueError if any required config key is missing or empty."""
    required = ("db_host", "db_name")

    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}"
        )


def connect(config: dict) -> None:
    """Simulate a database connection using the provided config."""
    print(f"[{config['log_level']}] Connecting to database...")
    print(f"  Host : {config['db_host']}:{config['db_port']}")
    print(f"  DB   : {config['db_name']}")
    print(f"\nActive configuration:\n{json.dumps(config, indent=2)}")


def main() -> None:
    config = load_config()
    validate_config(config)
    connect(config)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        raise SystemExit(1)





        




def load_config() -> dict:
    return {
        "db_host": os.environ.get("DB_HOST"),
        "db_port": int(os.getenv("DB_PORT", 5432)),
        "db_name": os.environ.get("DB_NAME"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }


def validate_config(config: dict) -> None:
    required = ("db_host", "db_name")

    for key in required:
        if not config.get(key):
            raise ValueError(
                f"Missing required configuration: {key}"
            )


def main() -> None:
    config = load_config()
    validate_config(config)

    print("Connecting to database...")
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()