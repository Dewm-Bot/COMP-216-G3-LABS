import threading
import time
import group_3_subscriber
import group_3_publisher

def run_sub():
    group_3_subscriber.subscribe()
def run_pub():
    group_3_publisher.publish()

if __name__ == "__main__":
    thread1 = threading.Thread(target=run_sub)
    thread2 = threading.Thread(target=run_pub)

    print("\n[Starting Subscriber]\n")
    thread1.start()
    print("\n[Waiting before starting publisher]\n")
    time.sleep(5)
    print("\n[Starting Publisher]\n")
    thread2.start()

    thread1.join()
    thread2.join()
