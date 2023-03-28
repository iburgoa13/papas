from django.test import TestCase
from django.urls import reverse
from .models import Customer, Product
class CustomerListTestCase(TestCase):
    
    def setUp(self):
        self.customer1 = Customer.objects.create(
            id=1,
            first_name='John',
            last_name='Doe',
        )
        self.customer2 = Customer.objects.create(
            id=2,
            first_name='Jane',
            last_name='Doe',
        )
    
    def test_customer_list_view(self):
        # Obtener la URL de la vista
        url = reverse('customer_list')
        
        # Realizar una petición GET a la URL
        response = self.client.get(url)
        
        # Verificar que la respuesta tiene un status code de 200
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se están mostrando todos los clientes en la respuesta
        self.assertContains(response, self.customer1.first_name)
        self.assertContains(response, self.customer1.last_name)
        self.assertContains(response, self.customer2.first_name)
        self.assertContains(response, self.customer2.last_name)
        
        # Verificar que se está utilizando la plantilla correcta
        self.assertTemplateUsed(response, 'customer_list.html')

class ProductListTest(TestCase):
    
    def setUp(self):
        # Creamos algunos productos para usar en los tests
        self.product1 = Product.objects.create(id=1,name='Producto 1', cost=10.0)
        self.product2 = Product.objects.create(id=2,name='Producto 2', cost=20.0)
    
    def test_product_list_view(self):
        # Hacemos una petición GET a la vista product_list
        response = self.client.get(reverse('product_list'))
        
        # Verificamos que la respuesta tiene un código HTTP 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Verificamos que la plantilla usada es la correcta
        self.assertTemplateUsed(response, 'product_list.html')
        
        # Verificamos que se muestran todos los productos en la base de datos
        products = response.context['products']
        self.assertEqual(len(products), 2)
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)