# Generated by Django 4.2.3 on 2023-10-11 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0007_rename_html_group_name_product_html_keywords_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='height',
        ),
        migrations.RemoveField(
            model_name='product',
            name='length',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='product',
            name='width',
        ),
    ]
