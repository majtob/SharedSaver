# Generated by Django 5.2.4 on 2025-07-22 06:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sharedaccount',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sharedaccount',
            name='members',
            field=models.ManyToManyField(through='accounts.AccountMembership', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accountmembership',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.sharedaccount'),
        ),
        migrations.AlterUniqueTogether(
            name='accountmembership',
            unique_together={('account', 'user')},
        ),
    ]
