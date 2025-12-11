import time
import socket

def check_connection():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except:
        return False

while True:
    if check_connection():
        print("Connected")
    else:
        print("Not Connected")
    time.sleep(5)
