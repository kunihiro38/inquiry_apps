from django.db import models

# これを中途半端に残すとLookUpErrorが出る
class Inquiry(models.Model):
    subject = models.CharField(verbose_name='name',
                                max_length=255)
    message = models.CharField(verbose_name='message',
                                max_length=500)
    email = models.EmailField(verbose_name="email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.subjects
