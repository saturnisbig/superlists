from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        req = HttpRequest()
        resp = home_page(req)
        expected_html = render_to_string('home.html')
        self.assertEqual(resp.content.decode(), expected_html)

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        resp = home_page(request)
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': request.POST['item_text']}
        )

        self.assertEqual(expected_html, resp.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item1 =  Item()
        item1.text = 'itemey 1'
        item1.save()

        item2 = Item()
        item2.text = 'itemey 2'
        item2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual('itemey 1', saved_items[0].text)
        self.assertEqual('itemey 2', saved_items[1].text)
