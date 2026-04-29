import json
from pathlib import Path

DEFAULT_RUNBOOKS = [
    {
        "id": "rb-001",
        "title": "Database Connection Pool Exhaustion",
        "keywords": [
            "connection pool exhausted",
            "db timeout",
            "acquire connection timed out",
        ],
        "actions": [
            {
                "step": 5,
                "action": "Inspect current DB active connections and long-running queries",
                "type": "investigation",
            },
            {
                "step": 6,
                "action": "Tune application connection pool and validate DB max_connections headroom",
                "type": "tuning",
            },
        ],
    }
]


def main() -> None:
    path = Path("data/runbooks.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(DEFAULT_RUNBOOKS, f, ensure_ascii=False, indent=2)
    print(f"Seeded runbooks into {path}")


if __name__ == "__main__":
    main()
