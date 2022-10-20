# Generated by Django 4.0 on 2022-10-20 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_order_customer_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]