from django.db import models

class Receipts(models.Model):
    receipts_name = models.CharField(max_length=200)
    receipts_date = models.DateTimeField('Purchased Date')
    total_price = models.IntegerField(default=0)
    raw_content = models.TextField()
    processed = models.BooleanField(default=False)
    invalid = models.BooleanField(default=False)
    fail_count = models.IntegerField(default=0)



class Item(models.Model):
    receipts = models.ForeignKey(Receipts, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=5000)
    item_quantity = models.IntegerField(default=1)
    item_price = models.IntegerField(default=0)


class SyncInfo(models.Model):
    user = models.CharField(max_length=200)
    time = models.DateTimeField('Time')