# Generated by Django 4.2.3 on 2023-10-17 11:36

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0013_product_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxySet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('proxies', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
        ),
        migrations.AddField(
            model_name='parseperiodictask',
            name='use_proxy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='use_proxy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parseperiodictask',
            name='proxy_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parser.proxyset'),
        ),
        migrations.AddField(
            model_name='task',
            name='proxy_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='parser.proxyset'),
        ),
    ]