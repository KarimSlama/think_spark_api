# Generated by Django 5.2 on 2025-05-13 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='userstatus',
            name='last_seen',
        ),
    ]
