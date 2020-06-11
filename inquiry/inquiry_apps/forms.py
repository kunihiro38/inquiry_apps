from django import forms

class InquiryAddForm(forms.Form):
    subject = forms.CharField(required=True,
                                max_length=255,)
