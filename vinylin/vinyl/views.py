from django.shortcuts import render
from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'vinyl/index.html')