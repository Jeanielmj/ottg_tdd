from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    # def test_home_page_doesnt_save_on_GET_request(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get('/lists/%d/' %(new_list.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        new_list = List.objects.create()
        Item.objects.create(text='itemey 1', list= new_list)
        Item.objects.create(text='itemey 2', list= new_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list= other_list)
        Item.objects.create(text='other item 2', list= other_list)

        response = self.client.get('/lists/%d/' %(new_list.id,))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        #other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_validation_errors_stay_on_list_page(self):
        current_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (current_list.id,),
            data={'item_text':''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error )

    def test_invalid_items_arent_saved(self):
        current_list = List.objects.create()
        self.client.post(
            '/lists/%d/' % (current_list.id,),
            data={'item_text':''}
        )
        self.assertEqual(Item.objects.count(), 0)

    def test_can_delete_item(self):
        new_list = List.objects.create()
        item_1 = Item.objects.create(text='itemey 1', list= new_list)
        item_2 = Item.objects.create(text='itemey 2', list= new_list)

        self.client.get('/lists/%d/%d/delete_item' % (new_list.id, item_1.id))
        self.assertEqual(Item.objects.count(), 1)

        self.client.get('/lists/%d/%d/delete_item' % (new_list.id, item_2.id))
        self.assertEqual(Item.objects.count(), 0)

    def test_list_view_displays_checkbox(self):
        current_list = List.objects.create()
        Item.objects.create(text='item 1', list= current_list)
        Item.objects.create(text='item 2', list= current_list)

        response = self.client.get('/lists/%d/' % (current_list.id,))

        self.assertContains(response, 'input type="checkbox"')

    def test_POST_items_marked_done(self):
        # Create list and items
        current_list = List.objects.create()
        item_1 = Item.objects.create(text='item 1', list= current_list)
        item_2 = Item.objects.create(text='item 2', list= current_list)

        # POST done
        response = self.client.post(
            '/lists/%d/items/' % (current_list.id,),
            data = {'mark_item_done': item_1.id
            }
        )
        # - including toggle items
        self.assertRedirects(response, '/lists/%d/' % (current_list.id,))
        item_1 = Item.objects.get(id=item_1.id)
        item_2 = Item.objects.get(id=item_2.id)
        # Check item is update
        self.assertTrue(item_1.is_done)
        self.assertFalse(item_2.is_done)

    def test_POST_multiple_items_done(self):
        current_list = List.objects.create()
        item_1 = Item.objects.create(text='item 1', list= current_list)
        item_2 = Item.objects.create(text='item 2', list= current_list)

        response = self.client.post(
            '/lists/%d/items/' % (current_list.id,),
            data = {'mark_item_done': [item_1.id, item_2.id]}
        )

        item_1 = Item.objects.get(id=item_1.id)
        item_2 = Item.objects.get(id=item_2.id)
        self.assertTrue(item_1.is_done)
        self.assertTrue(item_2.is_done)

    def test_POST_zero_items_done(self):
        current_list = List.objects.create()
        item_1 = Item.objects.create(text='item 1', list= current_list)
        item_2 = Item.objects.create(text='item 2', list= current_list)

        response = self.client.post(
            '/lists/%d/items/' % (current_list.id,),
            data = { }
        )

        item_1 = Item.objects.get(id=item_1.id)
        item_2 = Item.objects.get(id=item_2.id)
        self.assertFalse(item_1.is_done)
        self.assertFalse(item_2.is_done)

    def test_POST_items_toggles_done(self):
        # Create list and items
        current_list = List.objects.create()
        item_1 = Item.objects.create(
            text='item 1',
            list= current_list,
            is_done = True
            )

        item_2 = Item.objects.create(
            text='item 2',
            list= current_list,
            is_done = False
            )

        # POST done
        response = self.client.post(
            '/lists/%d/items/' % (current_list.id,),
            data = {'mark_item_done': item_2.id
            }
        )

        self.assertRedirects(response, '/lists/%d/' % (current_list.id,))

        item_1 = Item.objects.get(id=item_1.id)
        item_2 = Item.objects.get(id=item_2.id)
        self.assertFalse(item_1.is_done)
        self.assertTrue(item_2.is_done)

class NewListTest(TestCase):
    def test_save_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_are_sent_back_to_homepage(self):
        response = self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_new_list_has_name_of_first_item(self):
        response = self.client.post(
            '/lists/new',
            data = {'item_text': 'A new list item'
            })

        new_list = List.objects.first()
        self.assertEqual(new_list.name, 'A new list item')
