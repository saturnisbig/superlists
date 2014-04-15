from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    """docstring for home_page"""
    return HttpResponse('<html><title>To-Do lists</title></html>')
