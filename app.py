from pathlib import Path
import json
import os
from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = Path(os.environ.get("SERVICES_FILE", BASE_DIR / "services.json"))


def load_services():
    with DATA_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


# Filter values (category and search) may be at most this many characters long,
# measured after leading and trailing whitespace is removed.
MAX_FILTER_LENGTH = 50

app = Flask(__name__)


def read_filter(name):
    """Return a cleaned filter value, or None when the filter should be ignored.

    - Leading and trailing whitespace is removed.
    - A missing, empty, or whitespace-only value means "no filter" and is ignored.
    - A cleaned value longer than MAX_FILTER_LENGTH raises ValueError.
    """
    value = request.args.get(name)
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    if len(value) > MAX_FILTER_LENGTH:
        raise ValueError(f"{name} must be at most {MAX_FILTER_LENGTH} characters")
    return value


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/services")
def services():
    records = load_services()
    try:
        category = read_filter("category")
        search = read_filter("search")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    if category:
        records = [r for r in records if r["category"].lower() == category.lower()]
    if search:
        query = search.lower()
        records = [r for r in records if query in r["id"].lower() or query in r["name"].lower()]
    return jsonify(records)


@app.get("/services/<service_id>")
def service_by_id(service_id):
    record = next((r for r in load_services() if r["id"] == service_id), None)
    if record is None:
        return jsonify({"error": "service not found", "id": service_id}), 404
    return jsonify(record)


@app.get("/services/count")
def service_count():
    return jsonify({"count": len(load_services())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))