# Generated by Django 5.0 on 2024-04-04 11:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ias', '0010_aiparagraph'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AIparagraph',
            new_name='AI',
        ),
    ]