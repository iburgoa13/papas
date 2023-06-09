"""papas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from papas_app.views import import_customers, customer_list, home, import_products, product_list, import_orders, order_list, get_reporte_1,get_reporte_2, get_reporte_3

urlpatterns = [
    # Ruta para importar clientes desde un archivo CSV
    path('', home, name='home'),
    path('import-customers/', import_customers, name='import_customers'),
    path('import-product/', import_products, name='import_products'),
    path('import-order/', import_orders, name='import_orders'),

    # Ruta para mostrar la lista de clientes
    path('customer-list/', customer_list, name='customer_list'),
    path('product-list/', product_list, name='product_list'),
    path('order-list/', order_list, name='order_list'),
    path('generate-report-1/', get_reporte_1, name='get_reporte_1'),
    path('generate-report-2/', get_reporte_2, name='get_reporte_2'),
    path('generate-report-3/', get_reporte_3, name='get_reporte_3'),
]