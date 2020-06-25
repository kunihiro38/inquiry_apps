import re
import datetime
from django.test import TestCase
from .models import Inquiry

class InquiryViewTests(TestCase):
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
        # 白紙でリダイレクトされることもあるのできちんと中身もみてみるべき
        # ex)title、footer、bodyの中身にindexとか入れておくのも方法の一つ
        decoded_footer = re.findall(r'<small class="copy-right">©️ Inquiry apps<\/small>', res.content.decode()) 
        self.assertEqual('<small class="copy-right">©️ Inquiry apps</small>', decoded_footer[0])


        # go to inquiry form
        res = self.client.get(path='/inquiry/add/')
        self.assertEqual(res.status_code, 200)
        # ここもフォームがメインとかの、最低限の何か文言確認
        decoded_form = re.findall(r'<button type="submit"', res.content.decode())
        self.assertEqual('<button type="submit"', decoded_form[0])


        # go to inquiry and post
        # save just one data
        inquiry = {
            'name': 'test name',
            'subject': 'test subject',
            'message': datetime.datetime.now(), # 日付とか入れて
            'email': 'test@example.com',
            # created_at='',
            # updated_at='',
            'inquiry_status': Inquiry.InquiryStatus.Pending,
        }
        # ↑submitを押した状態
        res = self.client.post(path='/inquiry/add/', data=inquiry)

        # リダイレクト先が302
        self.assertEqual(res.status_code, 302)
        # 2.リダイレクト先がsuccess
        # res['Location] = res.url こっちでも可能
        self.assertEqual(res['Location'], '/inquiry/add/success/')

        # /inquiry/add/success/の確認
        res = self.client.get(path="/inquiry/add/success/")
        self.assertEqual(res.status_code, 200)


        # go to inquiry_list
        res = self.client.get(path='/inquiry/list/')
        self.assertEqual(res.status_code, 200)

        decoded_email = re.findall(inquiry['email'], res.content.decode())
        self.assertEqual(inquiry['email'], decoded_email[0])


        # go to comment list
        res = self.client.get(path='/inquiry/1/comment/list/')
        self.assertEqual(res.status_code, 200)
        
        

