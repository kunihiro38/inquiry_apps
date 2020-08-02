import datetime
from django.db import models


class InquiryStatus():
    Pending = 0
    Ignore = 1
    Completed = 2

    INQUIRY_STATUS_CHOICES = [
        (Pending, 'Pending'),
        (Ignore, 'Ignore'),
        (Completed, 'Completed')
    ]

    @classmethod
    def status_as_str(cls, inquiry_status):
        if inquiry_status == cls.Pending:
            return cls.INQUIRY_STATUS_CHOICES[0][1]
        
        elif inquiry_status == cls.Ignore:
            return cls.INQUIRY_STATUS_CHOICES[1][1]
        
        elif inquiry_status == cls.Completed:
            return cls.INQUIRY_STATUS_CHOICES[2][1]
        
        else:
            raise RuntimeError('invalid')
        


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

    inquiry_status = models.IntegerField(
        verbose_name='inquiry_status',
        choices=InquiryStatus.INQUIRY_STATUS_CHOICES,
        default=0
    )

    def inquiry_status_as_str(self):
        inquiry_status_as_str = InquiryStatus.status_as_str(self.inquiry_status)
        return inquiry_status_as_str


    def __str__(self):
        return self.subject

class InquiryComment(models.Model):
    class Meta:
        db_table = 'inquiry_comment'
    inquiry_id = models.IntegerField(verbose_name='inquiry_id',
                                        null=True,)

    user_id = models.IntegerField(verbose_name='user_id',
                                    null=True)

    created_at = models.DateTimeField(verbose_name='created_at',
                                        auto_now_add=True,)

    updated_at = models.DateTimeField(verbose_name='updated_at',
                                        auto_now=True,)

    inquiry_status = models.IntegerField(
        verbose_name='inquiry_status',
        choices=InquiryStatus.INQUIRY_STATUS_CHOICES,
        default=0
    )

    def inquiry_status_as_str(self):
        inquiry_status_as_str = InquiryStatus.status_as_str(self.inquiry_status)
        return inquiry_status_as_str


    comment = models.CharField(max_length=500)

    def __str__(self):
        return self.comment
