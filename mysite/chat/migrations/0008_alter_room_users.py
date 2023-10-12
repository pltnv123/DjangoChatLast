# Generated by Django 4.2.4 on 2023-10-10 17:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0007_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(blank=True, default=None, related_name='room_users', to=settings.AUTH_USER_MODEL),
        ),
    ]