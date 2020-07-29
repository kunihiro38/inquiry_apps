import re
import datetime
from django.test import TestCase, Client
from .models import Inquiry

# login
from django.contrib.auth.models import User

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
        
        

