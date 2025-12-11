Internet Monitor

Python script to monitor internet connection and log status changes.

Features
- Check connection every few seconds
- Detect status changes Connected or Not Connected
- Log changes with date and time to a file
- Show approximate uptime percentage
- Create HTML status page with current status and uptime
- Optional alerts sound email Telegram when internet is down for some time

How it works
- Tries to reach DNS server 8.8.8.8 on port 53
- When status changes it prints and logs the change
- Calculates uptime and downtime in seconds
- Writes status.html with latest info
- Sends alerts if connection stays down for ALERT_DOWN_SECONDS

Run
python monitor.py

Config
Edit values at top of monitor.py
- CHECK_INTERVAL_SECONDS
- ALERT_DOWN_SECONDS
- email settings if you enable email
- bot token and chat id if you enable Telegram

Files
- monitor.py        main script
- internet_log.txt  auto created log file
- status.html       auto created status page
