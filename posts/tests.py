import os
from pathlib import Path

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
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

    def tearDown(self):
        self.browser.quit()

    def test_should_open_chrome_window(self):
        self.browser.get(self.live_server_url)
