# Generated by Django 2.0.6 on 2018-12-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0007_auto_20181207_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(max_length=100),
        ),
    ]