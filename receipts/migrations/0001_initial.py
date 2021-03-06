# Generated by Django 2.1.2 on 2018-10-25 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=5000)),
                ('item_quantity', models.IntegerField(default=1)),
                ('item_price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipts_name', models.CharField(max_length=200)),
                ('receipts_date', models.DateTimeField(verbose_name='Purchased Date')),
                ('total_price', models.IntegerField(default=0)),
                ('raw_content', models.TextField()),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='receipts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipts.Receipts'),
        ),
    ]
