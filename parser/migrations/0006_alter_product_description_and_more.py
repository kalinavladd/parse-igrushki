# Generated by Django 4.2.3 on 2023-10-11 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0005_product_packing_method_uk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description_uk',
            field=models.TextField(blank=True, null=True),
        ),
    ]
