from django.db import transaction
from receipts.models import Receipts, Item
from bs4 import BeautifulSoup
from queue import Queue
import threading
import time

THREADS = 4
queue = Queue()


def process_raw_content():

    def valid_qty(x):
        try:
            return int(x.string) > 0
        except:
            return False

    def to_qty(x):
        return int(x.string)

    def to_price_int(x):
        return int(float(x.string.replace("$","")) * 100)

    r = queue.get()

    soup = BeautifulSoup(r.raw_content)

    # TODO: move specific path to a better place
    total_price = to_price_int(soup.table.table.table.thead.tr.td.string)

    item_qtys = list(map(to_qty, list(filter(valid_qty, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-qty")))))
    item_desc = list(map(lambda x: x.string, list(filter(lambda x: x.string, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-description")))))
    item_price = list(map(to_price_int,list(filter(lambda x: x.string, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-amount currency")))[1:]))

    print(total_price)
    print(len(item_desc))
    print(len(item_price))
    print(len(item_qtys))

    r.processed = True
    r.total_price = total_price
    update_processed_receipts(r, item_qtys, item_desc, item_price)

    queue.task_done()

@transaction.atomic
def update_processed_receipts(receipts, item_qtys, item_desc, item_price):
    existed = Receipts.objects.get(pk=receipts.pk)
    if existed.processed:
        return

    receipts.save()

    l = len(item_desc)
    if l != len(item_price) or l != len(item_qtys):
        raise Exception("Failed to parse a receipts")

    for i in range(l):
        Item.objects.create(receipts_id=receipts.id, item_name=item_desc[i], item_quantity=item_qtys[i],item_price=item_price[i])
    return


def fetch_all_unprocessed():
    while True:
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
