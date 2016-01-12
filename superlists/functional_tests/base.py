#from django.test import LiveServerTestCase
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import unittest

class ToDoFunctionalTest(StaticLiveServerTestCase):
    # before every test, set up
    def setUp(self):
        self.browser = webdriver.Firefox()
        # if anything every go wrong, after 3s, go ahead and fail right away
        self.browser.implicitly_wait(3)
    # after every test, shut down
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def enter_a_new_item(self, todo_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(todo_text)
        inputbox.send_keys(Keys.ENTER)
