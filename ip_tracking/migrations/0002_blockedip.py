# Generated by Django 5.2.4 on 2025-07-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ip_tracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
            ],
        ),
    ]
