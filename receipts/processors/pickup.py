from receipts.models import Receipts, Item
from bs4 import BeautifulSoup
from queue import Queue
import threading
import time

THREADS = 4
queue = Queue()


def process_raw_content():
    r = queue.get()
    soup = BeautifulSoup(r.raw_content)
    print(soup.table.tr.td.table.tr.td.table.thead.tr.td.string)
    queue.task_done()


def fetch_all_unprocessed():
    while(True):
        unprocessed = Receipts.objects.filter(processed=False)
        for r in unprocessed:
            queue.put_nowait(r)
        time.sleep(10)


def start_pickup():
    threads = []
    t = threading.Thread(target=fetch_all_unprocessed)
    t.start()
    threads.append(t)

    for i in range(THREADS):
        t = threading.Thread(target=process_raw_content)
        t.start()
        threads.append(t)
