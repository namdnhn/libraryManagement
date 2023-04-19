from django.shortcuts import render
from django.http import HttpResponse
import models

# Create your views here.
def index(request):
    return render(request, 'pages/home.html')