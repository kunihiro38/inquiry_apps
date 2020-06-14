from django.db import models

# これを中途半端に残すとLookUpErrorが出る
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
        max_length=1,
        choices=INQUIRY_STATUS_CHOICES,
        default=0
    )

    def __str__(self):
        return self.subject
