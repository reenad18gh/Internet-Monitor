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
Copy config example

bash
Copy code
cp config_example.py config.py
Edit config.py and add your Telegram and email settings

Run the monitor once

bash
Copy code
python monitor.py
Serve the web folder

bash
Copy code
cd web
python -m http.server 8000
Open http://localhost:8000 in your browser.

Automation
Use cron on Linux to run the monitor every minute

bash
Copy code
* * * * * /usr/bin/python3 /path/to/network-uptime-monitor/monitor.py
yaml
Copy code
