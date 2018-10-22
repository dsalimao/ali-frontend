from django.db import models

class Receipts(models.Model):
    receipts_name = models.CharField(max_length=200)
    receipts_date = models.DateTimeField('Purchased Date')
    total_price = models.IntegerField(default=0)
    raw_content = models.CharField(max_length=50000000)
    processed = models.BooleanField(default=False)


class Item(models.Model):
    receipts = models.ForeignKey(Receipts, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=5000)
    item_quantity = models.IntegerField(default=1)
    item_price = models.IntegerField(default=0)