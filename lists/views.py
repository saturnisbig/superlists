from django.shortcuts import render


def home_page(request):
    """docstring for home_page"""
    return render(request, 'home.html')
