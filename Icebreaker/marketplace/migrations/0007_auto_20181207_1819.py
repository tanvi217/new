# Generated by Django 2.0.6 on 2018-12-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_auto_20181207_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(help_text='This is Required', max_length=100),
        ),
    ]
