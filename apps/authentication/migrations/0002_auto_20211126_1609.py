# Generated by Django 3.1.7 on 2021-11-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
