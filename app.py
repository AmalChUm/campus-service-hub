from pathlib import Path
import json
import os
from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = Path(os.environ.get("SERVICES_FILE", BASE_DIR / "services.json"))


def load_services():
    with DATA_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/services")
def services():
    records = load_services()
    category = request.args.get("category")
    search = request.args.get("search")
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
