# Generated by Django 2.2 on 2020-08-31 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_apps', '0007_auto_20200830_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True, verbose_name='birthday'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_id',
            field=models.IntegerField(null=True, verbose_name='user_id'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avator',
            field=models.ImageField(default='images/default_icon.png', upload_to='images/', verbose_name='avator'),
        ),
    ]
