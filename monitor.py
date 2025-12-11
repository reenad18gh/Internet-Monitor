import time
import socket
import datetime
import smtplib
import ssl
import urllib.request
import urllib.parse
import json
import os

# اعدادات اساسية
CHECK_INTERVAL_SECONDS = 5
HOST = "8.8.8.8"
PORT = 53
TIMEOUT_SECONDS = 3
LOG_FILE = "internet_log.txt"
HTML_STATUS_FILE = "status.html"

# اعدادات التنبيه
ALERT_DOWN_SECONDS = 60          # بعد كم ثانية انقطاع يبدأ التنبيه

ENABLE_SOUND_ALERT = True
ENABLE_EMAIL_ALERT = False       # خليها True لو بتفعلي الايميل
ENABLE_TELEGRAM_ALERT = False    # خليها True لو بتفعلي تليجرام

# اعدادات الايميل
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 465
EMAIL_FROM = "you@example.com"
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"
EMAIL_TO = "you@example.com"

# اعدادات تليجرام
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"


def check_connection(host=HOST, port=PORT, timeout=TIMEOUT_SECONDS):
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        return True
    except OSError:
        return False


def log_status(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def play_sound_alert():
    try:
        import winsound
        winsound.Beep(1000, 1000)
    except Exception:
        # على الانظمة الاخرى استخدم beep بسيط
        print("\a")


def send_email_alert(subject, body):
    if not ENABLE_EMAIL_ALERT:
        return

    context = ssl.create_default_context()
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, context=context) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, message)
        print("Email alert sent")
    except Exception as e:
        print(f"Email failed {e}")


def send_telegram_alert(text):
    if not ENABLE_TELEGRAM_ALERT:
        return

    try:
        base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
        data_encoded = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(base_url, data=data_encoded)
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
        print("Telegram alert sent")
    except Exception as e:
        print(f"Telegram failed {e}")


def write_html_status(status_text, uptime_percent, up_time, down_time):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Internet Status</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        .status-up {{
            color: green;
            font-weight: bold;
        }}
        .status-down {{
            color: red;
            font-weight: bold;
        }}
        .box {{
            border: 1px solid #ddd;
            padding: 15px;
            max-width: 400px;
        }}
    </style>
</head>
<body>
    <h1>Internet Monitor</h1>
    <div class="box">
        <p>Last update {now}</p>
        <p>Status <span class="status-{"up" if status_text == "Connected" else "down"}">{status_text}</span></p>
        <p>Uptime {uptime_percent:.1f}%</p>
        <p>Up time {up_time} sec</p>
        <p>Down time {down_time} sec</p>
        <p>Refresh page to see new data</p>
    </div>
</body>
</html>
"""
    with open(HTML_STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(html)


def send_all_alerts(down_seconds):
    msg = f"Internet seems down for {down_seconds} seconds"

    if ENABLE_SOUND_ALERT:
        play_sound_alert()

    send_email_alert("Internet down alert", msg)
    send_telegram_alert(msg)


def main():
    last_status = None
    up_time = 0
    down_time = 0
    continuous_down_start = None
    alert_sent_for_this_down = False

    print("Starting internet monitor")
    print(f"Check every {CHECK_INTERVAL_SECONDS} seconds")
    print("Press Ctrl + C to stop")
    print("-" * 40)

    # انشئ ملف html في البداية
    write_html_status("Unknown", 0.0, 0, 0)

    while True:
        is_up = check_connection()
        now_dt = datetime.datetime.now()
        now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

        if is_up:
            up_time += CHECK_INTERVAL_SECONDS
            status_text = "Connected"

            # رجع العداد الخاص بالانقطاع
            continuous_down_start = None
            alert_sent_for_this_down = False
        else:
            down_time += CHECK_INTERVAL_SECONDS
            status_text = "Not Connected"

            if continuous_down_start is None:
                continuous_down_start = now_dt

        # سجل التغير في الحالة
        if last_status is None or last_status != is_up:
            line = f"[{now_str}] Status changed to {status_text}"
            print(line)
            log_status(line)
            last_status = is_up

        # احسب نسبة uptime
        total_time = up_time + down_time
        if total_time > 0:
            uptime_percent = (up_time / total_time) * 100
        else:
            uptime_percent = 0.0

        # اكتب حالة html
        write_html_status(status_text, uptime_percent, up_time, down_time)

        # تحقق من زمن الانقطاع وارسال التنبيه
        if not is_up and continuous_down_start is not None and not alert_sent_for_this_down:
            down_seconds = (now_dt - continuous_down_start).total_seconds()
            if down_seconds >= ALERT_DOWN_SECONDS:
                print()
                print(f"Alert internet down for {int(down_seconds)} seconds")
                send_all_alerts(int(down_seconds))
                alert_sent_for_this_down = True

        # عرض سطر حالة حي في التيرمنال
        print(
            f"Status {status_text}   "
            f"Uptime {uptime_percent:.1f}%   "
            f"Up {up_time} sec   Down {down_time} sec",
            end="\r"
        )

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    # انشئ ملف log لو مو موجود
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("Internet monitor log\n")
    main()
