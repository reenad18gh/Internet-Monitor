# Network Uptime Monitor

Small Python project to monitor internet connectivity, log uptime, send alerts, and show a simple HTML dashboard.

## How it works

- `monitor.py` runs a ping check to the target host
- Logs each check to `data/uptime_log.csv`
- Computes overall uptime percentage
- Writes the latest status to `web/status.json`
- Sends alerts to Telegram and email when the status changes

## Setup

1. Create virtual environment and install dependencies

   ```bash
   pip install -r requirements.txt
