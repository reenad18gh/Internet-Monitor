Internet Monitor

Python script to monitor internet connection and log status changes.

Features
- Check connection every few seconds
- Detect status changes Connected or Not Connected
- Log changes with date and time to a file
- Show approximate uptime percentage

How it works
- Tries to reach DNS server 8.8.8.8 on port 53
- When status changes it prints and logs the change
- Calculates uptime and downtime in seconds

Run
python monitor.py

Files
- monitor.py      main script
- internet_log.txt   auto created log file
