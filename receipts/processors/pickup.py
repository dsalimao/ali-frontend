from receipts.models import Receipts, Item
from _datetime import datetime


def on_pickup(name, raw):
    rdate = datetime.now()
    r = Receipts(receipts_name=name, receipts_date=rdate, raw_content=raw)
    r.save()



