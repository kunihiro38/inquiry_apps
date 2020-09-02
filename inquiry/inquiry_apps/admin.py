from django.contrib import admin
from .models import Inquiry, InquiryComment, UserProfile
from django.contrib.auth.models import User


admin.site.register(Inquiry)
admin.site.register(InquiryComment)
admin.site.register(UserProfile)



