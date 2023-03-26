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

from papas_app.views import import_customers, customer_list, home, import_products, product_list

urlpatterns = [
    # Ruta para importar clientes desde un archivo CSV
    path('', home, name='home'),
    path('import-customers/', import_customers, name='import_customers'),
    path('import-product/', import_products, name='import_products'),

    # Ruta para mostrar la lista de clientes
    path('customer-list/', customer_list, name='customer_list'),
    path('product-list/', product_list, name='product_list'),
]