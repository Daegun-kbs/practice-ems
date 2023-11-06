from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
import json
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

# 테스트 커버리지 80 이상
# 테스트는 public 으로 열려있으면 죄다 해야함
# 요청과 데이터 조회 테스트는 따로 할 수도있고, 같이 할 수도 있음

class ExampleTest(TestCase):
    def test_maths(self):
        self.assertEqual(1 + 1, 2)


# AJAX로 갱신되는 테이블 요청 테스트
class TableTests(TestCase):
    def test_maria_table(self):
        url = reverse("ems:ajax_update_table")
        data = {
            'page': '1',
            'start': '',
            'end': ''
            }
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)

    def test_influx_table(self):
        url = reverse("ems:ajax_update_table_influx")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_chart_table(self):
        url = reverse("ems:ajax_update_table_chart")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

# 차트 테스트
class ChartTest(TestCase):
    def chart(self):
        url = reverse("ems:chart_data")
        data = {
            'page': '1',
            'start': '',
            'end': ''
            }
        response = self.client.get(url, data)
        self.assertEquals(response.status_code, 200)


# 사용자 가입 로직 테스트
class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        # Given
        username = 'testuser'
        password1 = 'testpassword'
        password2 = 'testpassword'
        email = 'test@test.com'
        phone = '01000000000'

        # When
        url = reverse("common:signup")
        response = self.client.post(url, {'username': username, 'password1': password1, 'password2': password2, 'email': email, 'phone': phone})

        # Then
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username=username).exists())
