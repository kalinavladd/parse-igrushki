# Generated by Django 4.2.3 on 2023-10-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0008_remove_product_height_remove_product_length_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='height',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='length',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='width',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]