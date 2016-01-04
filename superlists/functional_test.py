from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    # before every test, set up
    def setUp(self):
        self.browser = webdriver.Firefox()
        # if anything every go wrong, after 3s, go ahead and fail right away
        self.browser.implicitely_wait(3)
    # after every test, shut down
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app
        # She notices the page title and header mention to-do lists.
        self. browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feather" into a text box
        # (Edith's hobby is tying fly-fishing lures)

        # When she hits enter, the page updates, and now the paske lists
        # "1. Buy peacock feathers" as an item in a to-do lists

        # There is still a text box inviting her to add another item.
        # She enters 'Use peacock feathers to make fly'
        # (Edith is very methodolical)

        # The homepage updates again, now shows both items on her lists
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site jas generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.

# main method
if __name__ == '__main__':
    # if this is python file being executed,
    unittest.main()
