# Generated by Django 4.2.3 on 2023-10-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_parseperiodictask_task_product_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_identificator',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='unique_identificator',
            field=models.PositiveIntegerField(default=0),
        ),
    ]