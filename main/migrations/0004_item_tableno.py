# Generated by Django 3.0.5 on 2021-06-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cartitems_tableno'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tableno',
            field=models.IntegerField(default=1),
        ),
    ]
