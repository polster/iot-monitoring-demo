#!/usr/bin/env python3
"""Generate JSON test messages for the IoT events data stream."""

from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from urllib import request


STATUSES = ["OK", "Warning", "Error"]


def random_location(lat: float, lon: float, jitter: float) -> dict:
    return {
        "lat": round(lat + random.uniform(-jitter, jitter), 6),
        "lon": round(lon + random.uniform(-jitter, jitter), 6),
    }


def generate_event(
    device_id: str,
    timestamp: datetime,
    base_lat: float,
    base_lon: float,
    jitter: float,
) -> dict:
    temperature = round(random.uniform(12.0, 32.0), 2)
    battery_level = round(random.uniform(10.0, 100.0), 1)
    status = random.choices(STATUSES, weights=[0.8, 0.15, 0.05], k=1)[0]

    return {
        "@timestamp": timestamp.isoformat().replace("+00:00", "Z"),
        "device_id": device_id,
        "temperature": temperature,
        "location": random_location(base_lat, base_lon, jitter),
        "battery_level": battery_level,
        "status": status,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate JSON lines for IoT event ingestion."
    )
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--device-prefix", default="device-")
    parser.add_argument("--device-count", type=int, default=3)
    parser.add_argument("--base-lat", type=float, default=47.3769)
    parser.add_argument("--base-lon", type=float, default=8.5417)
    parser.add_argument("--jitter", type=float, default=0.02)
    parser.add_argument("--minutes", type=int, default=30)
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--elastic-url", default="http://localhost:9200")
    parser.add_argument("--data-stream", default="iot-events")
    return parser.parse_args()


def bulk_ingest(elastic_url: str, data_stream: str, events: list[dict]) -> None:
    payload_lines = []
    for event in events:
        payload_lines.append(json.dumps({"index": {"_index": data_stream}}))
        payload_lines.append(json.dumps(event))

    payload = "\n".join(payload_lines) + "\n"
    url = f"{elastic_url.rstrip('/')}/_bulk"
    req = request.Request(
        url,
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/x-ndjson"},
        method="POST",
    )

    with request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        result = json.loads(body)

    if result.get("errors"):
        raise RuntimeError("Bulk ingest reported errors")


def main() -> None:
    args = parse_args()
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=args.minutes)

    events = []

    for i in range(args.count):
        device_id = f"{args.device_prefix}{(i % args.device_count) + 1}"
        ts = start + timedelta(seconds=i * (args.minutes * 60 / max(args.count, 1)))
        event = generate_event(device_id, ts, args.base_lat, args.base_lon, args.jitter)
        events.append(event)

    if args.ingest:
        bulk_ingest(args.elastic_url, args.data_stream, events)
        print(
            f"Ingested {len(events)} events into '{args.data_stream}' at {args.elastic_url}"
        )
        return

    for event in events:
        print(json.dumps(event, separators=(",", ":")))


if __name__ == "__main__":
    main()
