import datetime
from django.db import models

class Inquiry(models.Model):
    class Meta:
        db_table = 'inquiry'
    name = models.CharField(verbose_name='name',
                                max_length=255)
    subject = models.CharField(verbose_name='subject',
                                max_length=255)
    message = models.CharField(verbose_name='message',
                                max_length=500)
    email = models.EmailField(verbose_name='email')
    created_at = models.DateTimeField(verbose_name='created_at',
                                        auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='updated_at',
                                        auto_now_add=True)
    
    class InquiryStatus():
        Pending = 0
        Ignore = 1
        Completed = 2
    
    INQUIRY_STATUS_CHOICES = [
        (InquiryStatus.Pending, 'Pending'),
        (InquiryStatus.Ignore, 'Ignore'),
        (InquiryStatus.Completed, 'Completed'),
    ]

    inquiry_status = models.IntegerField(
        verbose_name='inquiry_status',
        choices=INQUIRY_STATUS_CHOICES,
        default=0
    )

    def __str__(self):
        return self.subject

class InquiryComment(models.Model):
    class Meta:
        db_table = 'inquiry_comment'
    inquiry_id = models.IntegerField(verbose_name='inquiry_id',
                                        null=True,)

    class PersonInCharge():
        Andrew = 0
        William = 1
        Emma = 2
    
    PERSON_IN_CHARGE_CHOICES = [
        (PersonInCharge.Andrew, 'Andrew'),
        (PersonInCharge.William, 'William'),
        (PersonInCharge.Emma, 'Emma'),
    ]
    pic = models.IntegerField(verbose_name='person_in_charge',
                            choices=PERSON_IN_CHARGE_CHOICES,
                            max_length=20,)
    pic_email = models.EmailField(verbose_name='pic_email',
                                    max_length=255)
    created_at = models.DateTimeField(verbose_name='created_at',
                                        auto_now_add=True,)

    updated_at = models.DateTimeField(verbose_name='updated_at',
                                        auto_now=True,)

    INQUIRY_STATUS_CHOICES = [
        (Inquiry.InquiryStatus.Pending, 'Pending'),
        (Inquiry.InquiryStatus.Ignore, 'Ignore'),
        (Inquiry.InquiryStatus.Completed, 'Completed'),
    ] 

    inquiry_status = models.IntegerField(
        verbose_name='inquiry_status',
        choices=INQUIRY_STATUS_CHOICES,
        default=0
    )
    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.pic
