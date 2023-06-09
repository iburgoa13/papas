import codecs
import csv
from django.contrib import messages
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Customer, Product, Order
from math import ceil

def validate_csv_file(csv_file):
    """
    Valida si el archivo subido por el usuario es un CSV.
    """
    if not csv_file.name.endswith('.csv'):
        raise Exception('El archivo seleccionado no es un archivo CSV.')

def validate_csv_header(header, expected_header):
    """
    Valida si el encabezado del CSV es correcto.
    """
    if header != expected_header:
        raise Exception(f"El archivo CSV debe tener exactamente tres columnas con los nombres de columna '{expected_header[0]}', '{expected_header[1]}' y '{expected_header[2]}', y en ese orden.")

def import_customer_row(row):
    """
    Crea un objeto Customer en la base de datos a partir de una fila del CSV.
    """
    try:
        if Customer.objects.filter(id=row[0]).exists():
            raise Exception(f"El cliente con id {row[0]} ya existe.")
        else:
            customer = Customer.objects.create(
                id=int(row[0]),
                first_name=row[1],
                last_name=row[2]
            )
            customer.save()
    except Exception as e:
        raise Exception(f"Error al importar el cliente con id {row[0]}: {e}")

def import_customers_from_csv(request, reader):
    """
    Importa los clientes de un archivo CSV subido por el usuario.
    """
    for row in reader:
        try:
            import_customer_row(row)
        except Exception as e:
            messages.error(request, str(e))
            continue

def import_customers(request):
    """
    Vista para importar clientes desde un archivo CSV subido por el usuario.
    """
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            validate_csv_file(csv_file)
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            header = next(reader)
            validate_csv_header(header,['id', 'firstname', 'lastname'])
            import_customers_from_csv(request, reader)
            return redirect('customer_list')    
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo CSV: {e}")
            return redirect('import_customers')

    return render(request, 'import_customers.html')

def import_product_row(row):
    """
    Crea un objeto Product en la base de datos a partir de una fila del CSV.
    """
    try:
        if Product.objects.filter(id=row[0]).exists():
            messages.error(f"El producto con id {row[0]} ya existe")
        else:
            product = Product.objects.create(
                id=int(row[0]),
                name=row[1],
                cost=ceil(float(row[2]) * 100) / 100
            )
            product.save()
    except Exception as e:
        messages.error(f"Error al importar el producto con id {row[0]}: {e}")

def import_products_from_csv(request,reader):
    """
    Importa los productos de un archivo CSV subido por el usuario.
    """
    for row in reader:
        try:
            import_product_row(row)
        except Exception as e:
            messages.error(request, str(e))
            continue

def import_products(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            validate_csv_file(csv_file)
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            header = next(reader)
            validate_csv_header(header,['id', 'name', 'cost'])
            import_products_from_csv(request,reader)
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo CSV: {e}")
            return redirect('import_products')
    return render(request, 'import_products.html')

def import_order_row(row):
    try:
        customer = get_object_or_404(Customer, id=row[1])
        product_ids = row[2].split(' ')
        print(product_ids)
        for product in product_ids:
            products = get_object_or_404(Product, id=product)
            order, created = Order.objects.get_or_create(id_order=row[0], customer=customer, product=products)
            if not created:
                order.amount += 1
                order.save()
    except Exception as e:
        messages.error(f"Error al importar la orden con id {row[0]}: {e}")


def import_orders_from_csv(request,reader):
    """
    Importa los orders de un archivo CSV subido por el usuario.
    """
    for row in reader:
        try:
            import_order_row(row)
        except Exception as e:
            messages.error(request, str(e))
            continue

def import_orders(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES['csv_file']
            validate_csv_file(csv_file)
            reader = csv.reader(codecs.iterdecode(csv_file, 'utf-8'))
            header = next(reader)
            validate_csv_header(header,['id', 'customer', 'products'])
            import_orders_from_csv(request,reader)
            return redirect('order_list')
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo CSV: {e}")
            return redirect('import_order')
    return render(request, 'import_order.html')


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def product_list(request):
    product = Product.objects.all()
    return render(request, 'product_list.html', {'products': product})

def order_list(request):
    order = Order.objects.all()
    return render(request, 'order_list.html', {'orders': order})

def home(request):
    return render(request, 'home.html')

def get_reporte_3(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_ranking.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'lastname', 'total'])

        customers = Customer.objects.annotate(
            total=Coalesce(
                Sum('order__amount', field='order__amount * order__product__cost'), 
                Value(0)
            )
        ).order_by('-total')

        for customer in customers:
            writer.writerow([customer.id, customer.first_name, customer.last_name, customer.total])

        return response

    except Exception as e:
        print(f"Error en la función 'get_reporte_3': {str(e)}")
        messages.error(request, 'Ha ocurrido un error al generar el reporte.')
        return redirect('home')

def get_reporte_2(request):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="product_customers.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'customer_ids'])

        products = Product.objects.all()

        for product in products:
            orders = Order.objects.filter(product=product)
            customer_ids = sorted(set(order.customer_id for order in orders))
            customers = ' '.join(str(customer_id) for customer_id in customer_ids)
            writer.writerow([product.id, customers])

        return response
    except Exception as e:
        print(f"Error en la función 'get_reporte_2': {str(e)}")
        messages.error(request, 'Ha ocurrido un error al generar el reporte.')
        return redirect('home')
    
def get_reporte_1(request):
    try:
        orders = Order.objects.all()
        id_orders = list(Order.objects.values_list('id_order', flat=True))
        order_totals = {}

        for ids_order in id_orders:
            total = 0
            orders = Order.objects.filter(id_order=ids_order)
            for order in orders:
                total += order.amount * order.product.cost
                order_totals[order.id_order] = total

        with open('order_prices.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            
            writer.writerow(['Order ID', 'Total (EUR)'])
            
            for order_id, total in order_totals.items():
                writer.writerow([order_id, total])
        
        with open('order_prices.csv', 'r') as file:
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=orders_prices.csv'
            return response

    except Exception as e:
        print(f"Error en la función 'get_reporte_1': {str(e)}")
        messages.error(request, 'Ha ocurrido un error al generar el reporte.')
        return redirect('home')