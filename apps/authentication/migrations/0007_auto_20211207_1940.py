# Generated by Django 3.1.7 on 2021-12-07 17:40

import apps.authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20211207_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/media/medoabdin/BE4C6BE74C6B98C3/Cources/upwork jobs/backend/Eng. Maher/notification&verification&user_image/website/django-backend/static/User/Images/default-logo.png', max_length=400, null=True, upload_to=apps.authentication.models.ProfileImage_Upload),
        ),
    ]