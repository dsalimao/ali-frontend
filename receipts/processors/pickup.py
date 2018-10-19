from receipts.models import Receipts, Item

def on_pickup(name, raw):
    r = Receipts(receipts_name=name, raw_content=raw)
    r.save()



