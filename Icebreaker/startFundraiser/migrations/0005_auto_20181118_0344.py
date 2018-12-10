# Generated by Django 2.0.6 on 2018-11-17 22:14

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startFundraiser', '0004_auto_20181116_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('description2', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, default='')),
            ],
        ),
        migrations.AlterField(
            model_name='campaign',
            name='image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]