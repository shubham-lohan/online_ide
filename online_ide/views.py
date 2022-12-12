from django.http import HttpResponse
from .models import *
from django.shortcuts import redirect, render


def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Hello</h1>")
