from receipts.models import Receipts, Item, SyncInfo

def delete_all():
    Receipts.objects.all().delete()
    SyncInfo.objects.all().delete()
    print("DELETED !!!!!!!!!!")