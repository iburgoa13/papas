from django.shortcuts import render
from .models import Customers

from django.http import HttpResponse

def testing(request):
    clientes = Customers.objects.all()
    return render(request, 'prueba.html', {'clientes': clientes})