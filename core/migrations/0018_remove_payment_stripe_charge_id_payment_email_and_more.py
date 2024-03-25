# Generated by Django 5.0.2 on 2024-03-21 10:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_payment_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='stripe_charge_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='ref',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]
