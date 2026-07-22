import requests
import threading
import time
import random

stop_flag = False


def send_requests(target):
    global stop_flag

    endpoints = ["/", "/index.html"]

    print("Traffic running - Press enter to stop")

    while not stop_flag:
        url = target + random.choice(endpoints)

        try:
            requests.get(url)
            print(f"{url}")
        except:
            pass

        time.sleep(1)


def wait_for_stop():
    global stop_flag
    input()
    stop_flag = True


def main():
    target = "http://webserver"

    t1 = threading.Thread(target=send_requests, args=(target,))
    t2 = threading.Thread(target=wait_for_stop)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Stopped.")


if __name__ == "__main__":
    main()