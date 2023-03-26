import codecs
import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer, Product
from io import TextIOWrapper
from math import ceil
def import_customers(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo seleccionado no es un archivo CSV.')
        else:
            # Abrir el archivo CSV en modo de texto
            
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            next(reader)
        for row in reader:
            if Customer.objects.filter(id=row[0]).exists():
                messages.error(request, f"El cliente con id {row[0]} ya existe")
                continue
            else:
                customer = Customer.objects.create(
                    id=int(row[0]),
                    first_name=row[1],
                    last_name=row[2]
                )
                customer.save()
        return redirect('customer_list')  # Redirige al usuario a la lista de clientes

    return render(request, 'import_customers.html')

def import_products(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo seleccionado no es un archivo CSV.')
        else:
            # Abrir el archivo CSV en modo de texto
            
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            next(reader)
        for row in reader:
            print(row)
            if Product.objects.filter(id=row[0]).exists():
                messages.error(request, f"El producto con id {row[0]} ya existe")
                continue
            else:
                product = Product.objects.create(
                    id=int(row[0]),
                    name=row[1],
                    cost=ceil(float(row[2]) * 100) / 100
                )
                print(product)
                product.save()
        return redirect('product_list')  # Redirige al usuario a la lista de produtos

    return render(request, 'import_products.html')

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def product_list(request):
    product = Product.objects.all()
    return render(request, 'product_list.html', {'products': product})

def home(request):
    return render(request, 'home.html')