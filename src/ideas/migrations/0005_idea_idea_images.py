# Generated by Django 5.2 on 2025-05-03 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0004_alter_ideaimage_options_remove_ideaimage_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='idea_images',
            field=models.ImageField(blank=True, null=True, upload_to='idea_photos/'),
        ),
    ]
