# Generated by Django 5.1.4 on 2025-01-02 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='uri',
            new_name='url',
        ),
    ]
