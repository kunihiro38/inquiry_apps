# Generated by Django 2.2 on 2020-06-29 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry_apps', '0002_inquirycomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquirycomment',
            name='inquiry_id',
            field=models.IntegerField(null=True, verbose_name='inquiry_id'),
        ),
        migrations.AddField(
            model_name='inquirycomment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='inquiry_status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Ignore'), (2, 'Completed')], default=0, verbose_name='inquiry_status'),
        ),
        migrations.AlterField(
            model_name='inquirycomment',
            name='inquiry_status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Ignore'), (2, 'Completed')], default=0, verbose_name='inquiry_status'),
        ),
    ]