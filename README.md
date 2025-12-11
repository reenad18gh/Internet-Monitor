# Internet Monitor

Python tool monitors internet connection and records every status change.  
Shows uptime, logs events, sends alerts, and generates a live HTML status page.

---

## Features

- Check connection every few seconds
- Detect status change (Connected or Not Connected)
- Log changes with date and time
- Show uptime percentage
- Auto-generate HTML status page
- Optional alerts  
  - sound  
  - email  
  - Telegram

---

## How it works

- Tries to reach DNS server 8.8.8.8 on port 53  
- Logs status changes  
- Tracks uptime and downtime  
- Writes live HTML file `status.html`  
- Sends alert when connection is down for `ALERT_DOWN_SECONDS`

---

## Demo

Status Page  
(Refresh manually to see new data)


