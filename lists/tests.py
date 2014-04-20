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


class ListViewTest(TestCase):

    def test_use_list_template(self):
        resp = self.client.get('/lists/the-unique-list-id/')
        self.assertTemplateUsed(resp, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        resp = self.client.get('/lists/the-unique-list-id/')

        self.assertContains(resp, 'itemey 1')
        self.assertContains(resp, 'itemey 2')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual('A new list item', new_item.text)

    def test_redirects_after_POST(self):
        resp = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertRedirects(resp, '/lists/the-unique-list-id/')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = 'itemey 1'
        item1.save()

        item2 = Item()
        item2.text = 'itemey 2'
        item2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual('itemey 1', saved_items[0].text)
        self.assertEqual('itemey 2', saved_items[1].text)
