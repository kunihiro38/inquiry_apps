# Generated by Django 2.2 on 2020-08-02 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_apps', '0004_auto_20200630_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquirycomment',
            name='pic',
        ),
        migrations.RemoveField(
            model_name='inquirycomment',
            name='pic_email',
        ),
        migrations.AddField(
            model_name='inquirycomment',
            name='user_id',
            field=models.IntegerField(null=True, verbose_name='user_id'),
        ),
    ]
