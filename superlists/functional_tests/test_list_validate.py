from unittest import skip
from .base import ToDoFunctionalTest

class ItemValidationTest(ToDoFunctionalTest):
    @skip("Haven't finish implementation")
    def test_cannot_add_empty_list_item(self):
        # Edith goes to homepage, and accidentally tries
        # to submit an empty list item
        # She hits "Enter" on the empty input box.

        # The homepage refreshes, and there is an error message
        # saying that list items cannot be blank.

        # Perversely tries to enter a second blank item.

        # She receives a similar warning on the list page.

        # And she can correct it by filling some text in.
        self.fail('Finish the test!')
