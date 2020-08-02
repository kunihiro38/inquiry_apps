from django.contrib import admin
from .models import Inquiry, InquiryComment

admin.site.register(Inquiry)
admin.site.register(InquiryComment)