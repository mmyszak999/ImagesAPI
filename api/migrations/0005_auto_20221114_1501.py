# Generated by Django 3.2 on 2022-11-14 14:01

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_image_image_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_height',
        ),
        migrations.RemoveField(
            model_name='image',
            name='image_width',
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=versatileimagefield.fields.VersatileImageField(upload_to='images/', verbose_name='Image'),
        ),
    ]