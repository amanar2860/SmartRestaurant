# Generated by Django 3.0.5 on 2021-06-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210606_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tableno',
            field=models.IntegerField(),
        ),
    ]
