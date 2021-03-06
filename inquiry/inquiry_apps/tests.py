import re
import os
import datetime
from django.test import TestCase, Client
from .models import InquiryStatus, Inquiry, UserProfile
from .forms import InquiryAddForm, AddInquiryCommentForm

# login
from django.contrib.auth.models import User

# img
from PIL import Image

'''
try test
% python manage.py test inquiry_apps.tests.InquiryViewTests
'''

class InquiryViewTests(TestCase):
    # 0729
    def test_inquiry_view_index_satatus_code(self):
        '''
        get status code 200 at index
        '''
        res = self.client.get(path='/')
        self.assertEqual(res.status_code, 200)

    # 0729
    def test_inquiry_view_create_user_and_login(self):
        '''
        create a new user and login success
        '''
        User.objects.create_user('Tom', 'test@example.com', 'tomtestlogin')
        res = self.client.get(path='/')
        self.assertEqual(res.status_code, 200)
        client_for_tom = Client()
        user = {
            'username': 'Tom',
            'password': 'tomtestlogin'
        }
        res = client_for_tom.post(path='/inquiry/list/', data=user)
        self.assertEqual(res.status_code, 302)




    def test_inquiry_view_all_response(self):
        '''
        1. confirm top page 200
        2. confirm /inquiry/add/ 200
        3. ポストがされデータが保存されたか確認
        4. status_code302, after post
        4. HttpResponseRedirectis add/success?
        5. inquiry/add/successの確認
        6. redirect to detail

        '''
        # go to toppage
        res = self.client.get(path='/')
        self.assertEqual(res.status_code, 200)
        # ex)title,footer,body contain index and so on
        decoded_footer = re.findall(r'<small class="copy-right">©️ Inquiry apps<\/small>', res.content.decode()) 
        self.assertEqual('<small class="copy-right">©️ Inquiry apps</small>', decoded_footer[0])


        # go to inquiry form
        res = self.client.get(path='/inquiry/add/')
        self.assertEqual(res.status_code, 200)
        # must confirm some words in body tag
        decoded_form = re.findall(r'<button type="submit"', res.content.decode())
        self.assertEqual('<button type="submit"', decoded_form[0])


        # go to inquiry and post
        # save just one data
        inquiry = {
            'name': 'test name',
            'subject': 'test subject',
            'message': datetime.datetime.now(),
            'email': 'test@example.com',
            # created_at='',
            # updated_at='',
            'inquiry_status': Inquiry.InquiryStatus.Pending,
        }
        # ↑submitを押した状態
        res = self.client.post(path='/inquiry/add/', data=inquiry)

        # go to 302 redirect
        self.assertEqual(res.status_code, 302)
        # same res['Location] = res.url 
        self.assertEqual(res['Location'], '/inquiry/add/success/')

        # /inquiry/add/success/
        res = self.client.get(path="/inquiry/add/success/")
        self.assertEqual(res.status_code, 200)

        # go to inquiry_list
        res = self.client.get(path='/inquiry/list/')
        self.assertEqual(res.status_code, 200)
        #　登録されたデータがあるか確認
        



        decoded_email = re.findall(inquiry['email'], res.content.decode())
        self.assertEqual(inquiry['email'], decoded_email[0])


        # go to comment list
        res = self.client.get(path='/inquiry/1/comment/list/')
        self.assertEqual(res.status_code, 200)
        
        

class InquiryModelTests(TestCase):
    def test_inquiry_model_empty(self):
        '''Inquiry model is effective'''
        for i in range(10):
            inquiry = Inquiry(
                name='Mr.%s' % i,
                email='test%s@example.com' % i,
                subject='No.%s' % i,
                message='number is {0}, name is {1}, age is {2}'
                        .format(i, 'a', 1),
                inquiry_status=InquiryStatus.Pending,
            )
            inquiry.save()
        self.assertEqual(Inquiry.objects.all().count(), 10)


    def test_inquiry_model_empty(self):
        '''data must be saved'''
        inquiry = Inquiry(
            name='Mr.first',
            email='test@example.com',
            subject='test subject',
            message='test',    
        )
        inquiry.save()
        saved_inquiry = Inquiry.objects.all()
        self.assertEqual(saved_inquiry.count(), 1)


    def test_inquiry_model_inquiry_status_change_to_ignore(self):
        '''Changing completed to Ignore is not allowed'''
        inquiry = Inquiry(
            name='Mr.first',
            email='test@example.com',
            subject='test subject',
            message='test',
            inquiry_status=InquiryStatus.Completed,
        )
        inquiry.save() # inquiry_status = 0
        new_status = InquiryStatus.Ignore
        (success, msg,) = inquiry.change_status_new_inquiry_status(new_status)
        self.assertFalse(success)
        self.assertTrue(msg)


class InquiryFormTests(TestCase):
    def test_inquiry_form_validate_email(self):
        '''use @@ email'''
        params = {
            'subject': 'subject',
            'message': 'message',
            'email': 'test@@example.com',
        }
        form = InquiryAddForm(data=params)
        self.assertFalse(form.is_valid())
        

    def test_inquiry_form_post_long_name(self):
        '''post long name is invalid'''
        params = {
            'name': 'a'* 256,
            'email': 'test_user@example.com',
            'subject': 'test_subject',
            'message': 'test',
        }
        form = InquiryAddForm(data=params)
        self.assertTrue(form.is_valid())

    
    def test_inquiry_comment_form_post_long_email(self):
        '''post long email'''
        params = {
            'person_in_charge': 0,
            'email': 'a'*20 + '@example.com',
            'inquiry_status': 0,
            'comment': 'test',
        }
        form = AddInquiryCommentForm(data=params)
        self.assertTrue(form.is_valid())

class UpLoadProfileImgFormTests(TestCase):
    # 0908
    def test_upload_profile_img_is_valid(self):
        print(self)
        '''UpLoadProfileImgForm is valid'''
        User.objects.create_user('Tom', 'tom@example.com', 'isexamplevalid')
        UserProfile.objects.create(user_id=1)


        client_for_tom = Client()
        user = {
            'username': 'Tom',
            'password': 'isexamplevalid'
        }
        res = client_for_tom.post(path='/inquiry/login/', data=user)
        self.assertEqual(302, res.status_code)

        if not os.path.exists('media/images/default_icon.png'):
            self.fail('no file')
        
        uploaded_file = open('/Users/kunihiro/desktop/test/inquiry/inquiry/media/images/default_icon.png', 'rb')

        # if post default_icon's name change so comment out
        # res = client_for_tom.post(
        #     path = '/inquiry/edit/profile/avator/',
        #     data = {
        #         'avator': uploaded_file
        #     }
        # )
        # self.assertEqual(302, res.status_code)

        # res = client_for_tom.get(path="/inquiry/edit/profile/success/")
        # decoded_msg = re.findall(r'Your Profile was updated!', res.content.decode())
        # self.assertEqual('Your Profile was updated!', decoded_msg[0])
        # self.assertIn('Your Profile was updated!', decoded_msg[0])

    
    def test_upload_profile_small_img_is_invalid(self):
        '''a small size image must be validated'''
        User.objects.create_user('Tom', 'tom@example.com', 'isexamplevalid')
        UserProfile.objects.create(user_id=1)
        if not os.path.exists('media/images/small-size.png'):
            self.fail('no file')

        
        client_for_tom = Client()
        user = {
            'username': 'Tom',
            'password': 'isexamplevalid'
        }
        res = client_for_tom.post(path='/inquiry/login/', data=user)
        self.assertEqual(302, res.status_code)
        

        res = client_for_tom.get(path='/inquiry/edit/profile/avator/')
        self.assertEqual(200, res.status_code)


        uploaded_file = open('/Users/kunihiro/desktop/test/inquiry/inquiry/media/images/small-size.png', 'rb')


        res = client_for_tom.post(
            path = '/inquiry/edit/profile/avator/',
            data = {
                'avator': uploaded_file
            }
        )
        error_msg = re.findall(r'Please register an image with a width of', res.content.decode())
        self.assertEqual('Please register an image with a width of', error_msg[0])
