from django.db import transaction
from receipts.models import Receipts, Item
from bs4 import BeautifulSoup
from queue import Queue
import threading
import time

THREADS = 10
queue = Queue()


def process_raw_content():
    while True:
        r = queue.get()
        try:
            print(r.receipts_name)
            if r.receipts_name.lower() == 'uber':
                uber(r)
            elif r.receipts_name.lower() == 'hmart':
                hmart(r)
            elif r.receipts_name.lower() == 'shell':
                shell(r)
            print('Receipts parsed')
        except Exception as e:
            r.fail_count += 1
            if r.fail_count >=2:
                r.invalid = True
            r.save()
            print(e)
        queue.task_done()
        time.sleep(1)

def shell(r):
    def to_price_int(x):
        return int(float(x.string.replace("$","").replace("=2E",".")) * 100)

    raw_content = r.raw_content
    body = raw_content[raw_content.index("<!DOCTYPE HTML"):]

    soup = BeautifulSoup(body)

    tds = soup.find_all(['td'])

    for i in range(len(tds)):
        if tds[i].string == 'TOTAL':
            p = to_price_int(tds[i+1].string)
            r.processed = True
            r.total_price = p
            update_processed_receipts(r, [1], ["Shell Fuel"], [p])
            break

def uber(r):
    def to_price_int(x):
        return int(float(x.string.replace("$","")) * 100)

    raw_content = r.raw_content
    body = raw_content[raw_content.lower().index("<!doctype html>"):]
    soup = BeautifulSoup(body)
    total_price = soup.table.tr.td.table.tr.td.table.tr.td.table.tr.td.table.tr.td.table.tr.td.table.tr.td.table.tr.td.\
        table.div.span.string

    r.processed = True
    r.total_price = to_price_int(total_price)
    update_processed_receipts(r, [1], ["Uber Rides"], [to_price_int(total_price)])


def hmart(r):
    def valid_qty(x):
        try:
            return int(x.string) > 0
        except:
            return False

    def to_qty(x):
        return int(x.string)

    def to_price_int(x):
        return int(float(x.string.replace("$","")) * 100)

    raw_content = r.raw_content
    body = raw_content[raw_content.index("<!DOCTYPE html>"):]
    soup = BeautifulSoup(body)

    # TODO: move specific path to a better place
    total_price = to_price_int(soup.table.table.table.thead.tr.td.string)

    item_qtys = list(map(to_qty, list(filter(valid_qty, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-qty")))))
    item_desc = list(map(lambda x: x.string, list(filter(lambda x: x.string, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-description")))))
    item_price = list(map(to_price_int,list(filter(lambda x: x.string, soup.find_all(['table','table','table','tbody', 'tr', 'td'],class_="item-amount currency")))[1:]))

    r.processed = True
    r.total_price = total_price
    update_processed_receipts(r, item_qtys, item_desc, item_price)


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
        unprocessed = Receipts.objects.filter(processed=False, invalid=False)
        for r in unprocessed:
            queue.put(r, block=True)
        time.sleep(30)


def start_pickup():
    threads = []
    t = threading.Thread(target=fetch_all_unprocessed)
    t.start()
    threads.append(t)

    for i in range(THREADS):
        t = threading.Thread(target=process_raw_content)
        t.start()
        threads.append(t)
