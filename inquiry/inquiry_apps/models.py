import datetime
from django.db import models




class UserProfile(models.Model):
    # user_id = models.IntegerField(
    #     verbose_name = 'user_id',
    #     null = False,
    # )
    
    avator = models.ImageField(
        verbose_name = 'avator',
        upload_to = 'images/',
        # default = 'images/default_icon.png'
    )

    # birthday = models.DateField(
    #     verbose_name = 'birthday',
    #     null=True,
    #     blank=False
    # )

    # def __init__(self):
    #     return self.user_id


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


    # only using test
    def change_status_new_inquiry_status(self, new_status):
        if not isinstance(new_status, int):
            raise ValueError('A value other than a character string has been assigned')

        all_inquiry_status = (InquiryStatus.Pending,
                                InquiryStatus.Ignore,
                                InquiryStatus.Completed)
        
        if not new_status in all_inquiry_status:
            raise ValueError('Value out of range is assigned')

        RET_KEEP = (True, 'keep status')
        RET_DENIED = (False, 'request denied')
        RET_COMPLETED = (True, 'status changed!')
        STATUS_CHANGED_DICT = {
            InquiryStatus.Pending:{
                InquiryStatus.Pending: RET_KEEP,
                InquiryStatus.Ignore: RET_DENIED,
                InquiryStatus.Completed: RET_COMPLETED,
            },
            InquiryStatus.Ignore:{
                InquiryStatus.Pending: RET_KEEP,
                InquiryStatus.Ignore: RET_DENIED,
                InquiryStatus.Completed: RET_COMPLETED,
            },
            InquiryStatus.Completed:{
                InquiryStatus.Pending: RET_KEEP,
                InquiryStatus.Ignore: RET_DENIED,
                InquiryStatus.Completed: RET_COMPLETED,
            }
        }
        (success, msg) = STATUS_CHANGED_DICT[self.inquiry_status][new_status]

        if success == True:
            self.inquiry_status = new_status
            self.save()
        return (success, msg,)


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
