# Generated by Django 3.2 on 2023-09-30 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_waiting',
            field=models.BooleanField(default=False),
        ),
    ]