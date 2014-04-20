from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import List, Item


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
        list_ = List.objects.create()
        resp = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(resp, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='Another list itemey 1', list=other_list)
        Item.objects.create(text='Another list itemey 2', list=other_list)

        resp = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(resp, 'itemey 1')
        self.assertContains(resp, 'itemey 2')
        self.assertNotContains(resp, 'Another list itemey 1')
        self.assertNotContains(resp, 'Another list itemey 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        resp = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(resp.context['list'], correct_list)


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

        new_list = List.objects.first()

        self.assertRedirects(resp, '/lists/%d/' % new_list.id)


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        resp = self.client.post(
            '/lists/%d/add_item' % correct_list.id,
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(resp, '/lists/%d/' % correct_list.id)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        item1 = Item()
        item1.text = 'itemey 1'
        item1.list = list_
        item1.save()

        item2 = Item()
        item2.text = 'itemey 2'
        item2.list = list_
        item2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('itemey 1', first_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual('itemey 2', second_saved_item.text)
        self.assertEqual(second_saved_item.list, list_)

