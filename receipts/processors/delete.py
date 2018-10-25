from receipts.models import Receipts, Item

def delete_all():
    Receipts.objects.all().delete()