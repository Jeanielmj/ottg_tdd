from .base import ToDoFunctionalTest
from selenium import webdriver

class DeleteItemTest(ToDoFunctionalTest):
    def test_delete_item(self):
        # self.browser.get(self.live_server_url)
        # self.enter_a_new_item('Itemey 1 to delete')
        # self.enter_a_new_item('Itemey 2 not to delete')
        #
        # self.check_for_row_in_list_table('1. Itemey 1 to delete')
        # self.check_for_row_in_list_table('2. Itemey 2 not to delete')
        #
        # item_1 = "Itemey 1 to delete"
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        #
        # for row in rows:
        #     if item_1 in row.text:
        #         print row.text
        #         row.find_element_by_tag_name('a').click()
        #
        # page_text = self.browser.find_element_by_tag_name('body').text
        # self.assertNotIn('Itemey 1 to delete', page_text)
        # self.assertIn('Itemey 2 not to delete', page_text)
        pass
