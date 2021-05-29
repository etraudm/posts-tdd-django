from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase


# Create your tests here.
from mixer.backend.django import mixer
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from posts.settings import env

class PostsTestCase(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(
            executable_path=env('CHROME_DRIVER'),
            options=options)

        self.test_user = mixer.blend(User)

    def tearDown(self):
        self.browser.quit()

