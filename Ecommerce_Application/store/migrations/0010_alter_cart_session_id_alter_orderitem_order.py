# Generated by Django 4.0 on 2022-10-19 22:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session_ID',
            field=models.CharField(default=uuid.uuid4, max_length=50),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
