from django import forms
from .models import InquiryComment
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                                max_length=255,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'User name'
                                    }
                                ),)
    
    password = forms.CharField(required=True,
                                max_length=255,
                                widget=forms.PasswordInput(
                                    attrs={
                                        'placeholder': 'Password'
                                    }
                                ))
                                

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            auth_result = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if not auth_result:
                raise ValidationError('Wrong username or password')
        return cleaned_data


    def clean_username(self):
        username = self.cleaned_data['username']

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

class InquiryAddForm(forms.Form):
    name = forms.CharField(required=True,
                            max_length=255,)
    email = forms.EmailField(required=True,
                              max_length=255,)
    subject = forms.CharField(required=False,
                                max_length=255,)
    message = forms.CharField(required=True,
                                max_length=1000,
                                widget=forms.Textarea(
                                    attrs={
                                        'placeholder': 'input some words',
                                    }
                                ),)

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

class InquiryFindForm(forms.Form):
    id = forms.IntegerField(required=False,
                                min_value=1,
                                max_value=100000)
    email = forms.CharField(required=False,
                                max_length=255)
    page = forms.IntegerField(required=False,
                                max_value=10000,
                                min_value=1,)
    word = forms.CharField(required=False,
                            max_length=1000)
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_id(self):
        find_id = self.cleaned_data['id']
        return find_id
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_page(self):
        page =self.cleaned_data['page']
        if page == None:
            page = 1
        return page
    
    def clean_word(self):
        word = self.cleaned_data['word']
        return word

class AddInquiryCommentForm(forms.Form):
    PERSON_IN_CHARGE_CHOICES = (
        ("", ""),
        (InquiryComment.PersonInCharge.Andrew, 'Andrew'),
        (InquiryComment.PersonInCharge.William, 'William'),
        (InquiryComment.PersonInCharge.Emma, 'Emma'),
    )
    person_in_charge = forms.fields.ChoiceField(
                                        choices = PERSON_IN_CHARGE_CHOICES,
                                        required=False,
                                        widget=forms.widgets.Select,)
    email = forms.EmailField(required=True,
                                max_length=255,)

    inquiry_status = forms.fields.ChoiceField(
                                    choices = InquiryComment.INQUIRY_STATUS_CHOICES,
                                    widget=forms.widgets.Select,
                                    )
    comment = forms.CharField(required=True,
                            max_length=1000,
                            widget=forms.Textarea(
                                attrs={
                                    'placeholder': 'what you did',
                                }))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_person_in_charge(self):
        person_in_charge = self.cleaned_data['person_in_charge']
        return person_in_charge
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_inquiry_status(self):
        inquiry_status = self.cleaned_data['inquiry_status']
        return inquiry_status
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        return comment





class EditInquiryCommentForm(forms.Form):
    inquiry_status = forms.fields.ChoiceField(
                                    choices = InquiryComment.INQUIRY_STATUS_CHOICES,
                                    widget=forms.widgets.Select,
                                    )
    comment = forms.CharField(required=True,
                                    max_length=1000,
                                    widget=forms.Textarea()
                                    )


    def __init__(self, inquiry_id, comment_id, *args, **kwargs):
        # __init__設置理由は、
        # ※After updating, you will not be able to re-update 10 minutes after updating.
        # 上を発動させるために、modelのupdated_atを取得するために作成
        # *args tuple
        # **kwargs 辞書方オブジェクト

        self.inquiry_id = inquiry_id
        self.comment_id = comment_id
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()
        current_time_utc = datetime.now(timezone.utc)
        qs = InquiryComment.objects.get(id=self.comment_id)
        updated_at_plus_some_min = qs.updated_at + timedelta(minutes=(10))
        if current_time_utc < updated_at_plus_some_min:
            raise forms.ValidationError('After updating, you will not be able to re-update 10 minutes after updating.')
        return cleaned_data

    def clean_inquiry_status(self):
        latest_inquiry_comment = InquiryComment.objects.get(id=self.comment_id)
        inquiry_status = int(self.cleaned_data['inquiry_status'])
        if latest_inquiry_comment.inquiry_status == 2 and inquiry_status == 1:
            raise forms.ValidationError('You cannot change from "Completed" to "Ignore"')
        return inquiry_status
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        return comment
