# Generated by Django 4.2.5 on 2023-10-30 16:52

from django.db import migrations, models
import newapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0008_remove_product_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image1',
            field=models.ImageField(blank=True, null=True, upload_to=newapp.models.get_file_path),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image2',
            field=models.ImageField(blank=True, null=True, upload_to=newapp.models.get_file_path),
        ),
        migrations.AddField(
            model_name='product',
            name='product_image3',
            field=models.ImageField(blank=True, null=True, upload_to=newapp.models.get_file_path),
        ),
    ]