import time
import socket
import datetime

CHECK_INTERVAL_SECONDS = 5      # كم ثانية بين كل فحص
HOST = "8.8.8.8"                # السيرفر اللي نفحص عليه
PORT = 53                       # بورت DNS
TIMEOUT_SECONDS = 3             # مهلة الاتصال
LOG_FILE = "internet_log.txt"   # ملف التخزين


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


def main():
    last_status = None
    up_time = 0
    down_time = 0
    start_time = time.time()

    print("Starting internet monitor")
    print(f"Check every {CHECK_INTERVAL_SECONDS} seconds")
    print("Press Ctrl + C to stop")
    print("-" * 40)

    while True:
        is_up = check_connection()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_up:
            up_time += CHECK_INTERVAL_SECONDS
            status_text = "Connected"
        else:
            down_time += CHECK_INTERVAL_SECONDS
            status_text = "Not Connected"

        # اطبع وسجل فقط إذا تغيرت الحالة
        if last_status is None or last_status != is_up:
            line = f"[{now}] Status changed to {status_text}"
            print(line)
            log_status(line)
            last_status = is_up

        # احسب نسبة الـ uptime بشكل تقريبي
        total_time = up_time + down_time
        if total_time > 0:
            uptime_percent = (up_time / total_time) * 100
            print(
                f"Uptime {uptime_percent:.1f}%   "
                f"Up {up_time} sec   Down {down_time} sec",
                end="\r"
            )

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
