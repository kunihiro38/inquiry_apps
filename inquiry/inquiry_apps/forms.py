from django import forms

class InquiryAddForm(forms.Form):
    name = forms.CharField(required=True,
                            max_length=255,)
    email = forms.EmailField(required=True,
                              max_length=255,)
    subject = forms.CharField(required=False,
                                max_length=255,)
    message = forms.CharField(required=True,
                                max_length=1000,
                                widget=forms.Textarea,)
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    
    def clean_subject(self):
        subject = self.cleaned_data['subject']
        return subject
    
    def clean_message(self):
        message = self.cleaned_data['message']
        return message

class InquiryFindForm(forms.form):
    id = forms.IntegerField(required=False,
                                min_value=1,
                                max_value=100000)
    subject = forms.CharField(required=False,
                                max_length=255)
    word = forms.CharField(required=False,
                            max_length=1000)