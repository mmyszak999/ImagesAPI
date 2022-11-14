# Generated by Django 3.2 on 2022-11-14 13:54

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_image_thumbnails_remove_thumbnail_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=versatileimagefield.fields.VersatileImageField(upload_to='images/', verbose_name='Image'),
        ),
    ]
