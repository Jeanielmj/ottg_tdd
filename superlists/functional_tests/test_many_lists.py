from .base import ToDoFunctionalTest

class ManyListsTest(ToDoFunctionalTest):
    def change_list_name(self, list_name):
        inputbox = self.browser.find_element_by_id('id_rename_list')
        inputbox.clear()
        inputbox.send_keys(list_name + '\n')

    def test_can_create_and_view_multiple_lists(self):
        self.browser.get(self.live_server_url)
        # Edith comes to the homepage, creates a new list,
        # and fills in her grocery list.
        self.enter_a_new_item('Buy milk')
        self.enter_a_new_item('Buy cheese')
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')

        # She sees she can change a list name
        self.change_list_name('Groceries')

        # Edith goes back to the home page $ sees her grocery list
        self.browser.get(self.live_server_url)
        self.check_for_row_in_list_table('Groceries')

        import time
        time.sleep(15)
        # Edith creates a new list for her Art History homework
        self.enter_a_new_item('Read Camille')

        time.sleep(10)
        # Edith opens the home page later & sees both lists
        self.browser.get(self.live_server_url)

        time.sleep(10)
        self.check_for_row_in_list_table('Groceries')
        self.check_for_row_in_list_table('Read Camille')

        # Edith does to the grocey list and sees what she needs to buy.
        row = self.find_table_row('Groceries')
        row.find_element_by_tag_name('a').click()
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')
