import csv
import datetime as dt
import json
import os
import subprocess
from typing import Optional, Tuple

import alerts
import config


DATA_DIR = "data"
WEB_DIR = "web"
LOG_PATH = os.path.join(DATA_DIR, "uptime_log.csv")
STATUS_JSON_PATH = os.path.join(WEB_DIR, "status.json")


def ensure_directories() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(WEB_DIR, exist_ok=True)


def ping_host(host: str) -> bool:
    """
    Returns True if host responds to ping
    Uses one ping with short timeout
    """
    try:
        # -c 1 one packet
        # -W 2 timeout 2 seconds (Linux)
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False


def read_last_status(log_path: str) -> Optional[str]:
    if not os.path.isfile(log_path):
        return None

    last_row = None
    try:
        with open(log_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                last_row = row
    except Exception:
        return None

    if last_row is None:
        return None
    return last_row.get("status")


def append_log(
    log_path: str,
    timestamp: str,
    status: str,
    response_ms: Optional[float],
) -> None:
    file_exists = os.path.isfile(log_path)

    fieldnames = ["timestamp_utc", "status", "response_ms"]

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp_utc": timestamp,
                "status": status,
                "response_ms": f"{response_ms:.2f}" if response_ms is not None else "",
            }
        )


def compute_uptime(log_path: str) -> Tuple[float, int, int]:
    if not os.path.isfile(log_path):
        return 0.0, 0, 0

    total = 0
    up = 0
    down = 0

    try:
        with open(log_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                if row.get("status") == "UP":
                    up += 1
                elif row.get("status") == "DOWN":
                    down += 1
    except Exception:
        return 0.0, 0, 0

    if total == 0:
        return 0.0, 0, 0

    uptime_percentage = (up / total) * 100.0
    return uptime_percentage, total, down


def write_status_json(
    json_path: str,
    timestamp: str,
    status: str,
    uptime_percentage: float,
    total_checks: int,
    down_checks: int,
) -> None:
    payload = {
        "timestamp_utc": timestamp,
        "status": status,
        "uptime_percentage": round(uptime_percentage, 2),
        "total_checks": total_checks,
        "down_checks": down_checks,
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def main() -> None:
    ensure_directories()

    host = getattr(config, "HOST_TO_PING", "8.8.8.8")

    now = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    is_up = ping_host(host)
    status = "UP" if is_up else "DOWN"

    # simple response time placeholder
    response_ms = None
    if is_up:
        # you can extend this later to measure real latency
        response_ms = 1.0

    last_status = read_last_status(LOG_PATH)

    append_log(LOG_PATH, now, status, response_ms)

    uptime_percentage, total, down = compute_uptime(LOG_PATH)

    write_status_json(
        STATUS_JSON_PATH,
        now,
        status,
        uptime_percentage,
        total,
        down,
    )

    if status == "DOWN" and last_status != "DOWN":
        message = f"Network is DOWN for {host} at {now}"
        alerts.send_alert(message)
    elif status == "UP" and last_status == "DOWN":
        message = (
            f"Network is back UP for {host} at {now}. "
            f"Current uptime: {uptime_percentage:.2f}%"
        )
        alerts.send_alert(message)


if __name__ == "__main__":
    main()
