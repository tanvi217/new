# Generated by Django 2.0.5 on 2018-12-01 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_auto_20181202_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cost',
            field=models.FloatField(null=True),
        ),
    ]
