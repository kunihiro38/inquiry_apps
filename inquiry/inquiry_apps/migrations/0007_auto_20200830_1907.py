# Generated by Django 2.2 on 2020-08-30 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_apps', '0006_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avator',
            field=models.ImageField(upload_to='media/', verbose_name='avator'),
        ),
    ]
