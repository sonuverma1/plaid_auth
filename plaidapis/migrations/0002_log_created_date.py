# Generated by Django 3.1.6 on 2021-02-03 19:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('plaidapis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]