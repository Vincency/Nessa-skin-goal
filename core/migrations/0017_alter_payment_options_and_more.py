# Generated by Django 5.0.2 on 2024-03-20 11:18

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_payment_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='date_created',
            new_name='timestamp',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='ref',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='verified',
        ),
        migrations.AddField(
            model_name='payment',
            name='stripe_charge_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserWallet',
        ),
    ]
