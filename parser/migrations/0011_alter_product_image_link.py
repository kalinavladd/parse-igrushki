# Generated by Django 4.2.3 on 2023-10-11 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0010_task_errors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]