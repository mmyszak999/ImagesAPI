# Generated by Django 3.2 on 2022-11-14 13:59

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20221114_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=versatileimagefield.fields.VersatileImageField(upload_to='images', verbose_name='Image'),
        ),
    ]
