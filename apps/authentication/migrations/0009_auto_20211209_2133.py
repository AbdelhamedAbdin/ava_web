# Generated by Django 3.1.7 on 2021-12-09 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20211207_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='verificationkey',
            old_name='key',
            new_name='code',
        ),
        migrations.RemoveField(
            model_name='verificationkey',
            name='updated_at',
        ),
    ]
