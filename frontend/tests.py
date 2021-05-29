import time

from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase


# Create your tests here.
from mixer.backend.django import mixer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from posts.settings import env

class PostsTestCase(LiveServerTestCase):

    def setUp(self):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(
            executable_path=env('CHROME_DRIVER'),
            options=options)
        #mock user
        self.test_user: User = mixer.blend(User, password='123')

    def tearDown(self):
        self.browser.quit()


    # def test_should_login_with_username_and_password(self):
    #     self.browser.get(self.live_server_url)
    #     time.sleep(5)
    #     btnLogin = self.browser.find_element_by_id('btn-open-modal-login')
    #     btnLogin.click()
    #     time.sleep(1)
    #
    #     password = self.browser.find_element_by_id('password-login')
    #     username = self.browser.find_element_by_id('email-login')
    #     btnSubmit = self.browser.find_element_by_id('btn-login')
    #
    #     username.send_keys(self.test_user.username)
    #     password.send_keys(self.test_user.password)
    #
    #     btnSubmit.click()
    #
    #
    #     self.browser.get(self.live_server_url)

