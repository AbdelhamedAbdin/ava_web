# Generated by Django 3.1.7 on 2021-12-09 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_verificationkey_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=400)),
            ],
        ),
    ]
