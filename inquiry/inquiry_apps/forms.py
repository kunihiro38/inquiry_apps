from django import forms
from .models import InquiryComment, InquiryStatus
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

from django.contrib.admin.widgets import AdminDateWidget

# images
from PIL import Image

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usernam',
                'class': 'input-field',
            }
        ))
    
    password = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
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
    name = forms.CharField(
        required=True,
        max_length=255,)
    email = forms.EmailField(
        required=True,
        max_length=255,)
    subject = forms.CharField(
        required=False,
        max_length=255,)
    message = forms.CharField(
        required=True,
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


class AddUserForm(forms.Form):
    username = forms.CharField(
        required = True,
        max_length = 150,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'name',
                'class': '',
            }
        )
    )

    email = forms.EmailField(
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Your email',
                'class': '',
            }
        )
    )

    birthday = forms.DateField(
        required =True,
        widget = forms.SelectDateWidget(
            years = range(1950, 2017)
        )
    )

    password = forms.CharField(
        required = True,
        max_length=255,
        min_length=6,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    confirm_password = forms.CharField(
        required = True,
        max_length=255,
        min_length=6,
        widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm_Password'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        return birthday

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if confirm_password != self.cleaned_data['password']:
            raise ValidationError('Passwords do not match')
        return confirm_password


class UpLoadProfileImgForm(forms.Form):
    avator = forms.ImageField(required=True)
    def clean_avator(self):
        '''
        1.filev形式
        2.サイズ確認
        3.ファイルサイズ確認

        '''
        avator = self.cleaned_data['avator']

        if not avator:
            raise ValidationError('not images')

        IMG_WIDTH = 200
        if avator.image.width < IMG_WIDTH:
            raise ValidationError(
                'The width of this image is %spx. \
                Please register an image with a width of %spx or more.' \
                % (avator.image.width, IMG_WIDTH)
            )

        IMG_HEIGHT = 200
        if avator.image.height < IMG_HEIGHT:
            raise ValidationError(
                'The heigth of this image is %spx. \
                Please register an image with a height of %spx or more.' \
                % (avator.image.width, IMG_WIDTH)
            )

        IMG_SIZE = 2*1000*1000
        if avator.size > IMG_SIZE:
            raise ValidationError(
                '画像サイズが大きすぎます。%sMBより小さいサイズの画像をお願いします。' \
                % str(IMG_SIZE//1000//1000)
            )


        return avator




class EditProfileForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length='150',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
                'class': 'input-field'
            }
        ))
    email = forms.EmailField(
        required=True,
        max_length='255',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'email',
                'class': 'input-field'
            }
        ))
    current_password = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '',
                'class': 'input-field'
            }
        ))
    new_password = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '',
                'class': 'input-field'
            }
        ))
    confirm_new_password = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '',
                'class': 'input-field'
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data['username']
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_current_password(self):
        password = self.cleaned_current_data['password']
        return password


class EditProfileUsernameForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(
            attrs={

            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        return username


class EditProfileEmailForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=255,
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        return email


class EditProfilePasswordForm(forms.Form):
    current_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(
        )
    )

    new_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(
        )
    )

    confirm_new_password = forms.CharField(
        required=True,
        max_length=255,
        min_length=6,
        widget=forms.PasswordInput(
        )
    )

    def __init__(self, _user_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_name = _user_name
    
    def clean(self):
        cleaned_data = super(EditProfilePasswordForm, self).clean()
        print(cleaned_data)
        return cleaned_data

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if self._user_name and current_password:
            auth_result = authenticate(
                username = self._user_name,
                password=current_password
            )
            if not auth_result:
                raise ValidationError('Password is incorrect')
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        return new_password
    
    def clean_confirm_new_password(self):
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if confirm_new_password != self.cleaned_data['new_password']:
            raise ValidationError('Passwords do not match')
        return confirm_new_password


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
    inquiry_status = forms.fields.ChoiceField(
                                    choices = InquiryStatus.INQUIRY_STATUS_CHOICES,
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

    def clean_inquiry_status(self):
        inquiry_status = self.cleaned_data['inquiry_status']
        return inquiry_status
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        return comment





class EditInquiryCommentForm(forms.Form):
    inquiry_status = forms.fields.ChoiceField(
                                    choices = InquiryStatus.INQUIRY_STATUS_CHOICES,
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
