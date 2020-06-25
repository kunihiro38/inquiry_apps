import re
import datetime
from django.test import TestCase
from .models import Inquiry

class InquiryViewTests(TestCase):
    def test_inquiry_view_all_response(self):
        '''
        1. confirm top page 200
        2. confirm /inquiry/add/ 200
        '''
        # go to toppage
        res = self.client.get(path='/')
        self.assertEqual(res.status_code, 200)
        # きちんと中身もみてみるべき ex)indexとかbase.htmlとか、title, footerとか
        # bodyの中身にindexとか入れておくのもて
        decoded_footer = re.findall(r'<small class="copy-right">©️ Inquiry apps<\/small>', res.content.decode()) 
        self.assertEqual('<small class="copy-right">©️ Inquiry apps</small>', decoded_footer[0])


        # go to inquiry form
        res = self.client.get(path='/inquiry/add/')
        self.assertEqual(res.status_code, 200)
        # ここもフォームがメインとかの、最低限の何か文言確認
        decoded_form = re.findall(r'<button type="submit"', res.content.decode())
        self.assertEqual('<button type="submit"', decoded_form[0])


        # go to inquiry_list
        # save just one data
        inquiry = {
            'name': 'test name',
            'subject': 'test subject',
            'message': datetime.datetime.now(), # 日付とか入れっる
            'email': 'test@example.com',
            # created_at='',
            # updated_at='',
            'inquiry_status': Inquiry.InquiryStatus.Pending,
        }
        # ↑submitを押した状態
        res = self.client.post(path='/inquiry/add/', data=inquiry)
        # ここでデータが作成できたか確認、id、
        # print(Inquiry.objects.values())

        # /inquiry/ass/success/ ↓
        # html　上に登録されたばかりのid番号を入れておく
        # viewsでidを取得して、dataをテンプレートタグに入れれば完結できると思ったけど
        # viewsの可読性が下がりそう・・・
        res = self.client.get(path="/inquiry/add/success/")
        print(res)
        print(res.content.decode())
        self.assertEqual(res.status_code, 200)