from django.test import TestCase
from django.urls import reverse
from .models import Customer, Product, Order
from io import StringIO
from .views import validate_csv_file,validate_csv_header, import_customer_row, import_product_row,import_order_row
from unittest.mock import patch, Mock, call
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from django.test import RequestFactory
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

class ImportCustomerTest(TestCase):
    
    def test_validate_csv_file(self):
        # Test case 1: archivo CSV subido correctamente
        csv_file = SimpleUploadedFile("file.csv", b"file_content", content_type="text/csv")
        try:
            validate_csv_file(csv_file)
        except Exception:
            assert False, "Debería haber pasado la validación, ya que es un archivo CSV."
        
        # Test case 2: archivo no CSV subido
        txt_file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        try:
            validate_csv_file(txt_file)
        except Exception as e:
            self.assertEqual(str(e),"El archivo seleccionado no es un archivo CSV.")
    
    def test_validate_csv_header(self):
    # Test case 1: encabezado del archivo CSV es correcto
        good_header = ['id', 'firstname', 'lastname']
        expected_header = ['id', 'firstname', 'lastname']
        try:
            validate_csv_header(good_header,expected_header)
        except Exception:
            assert False, "Debería haber pasado la validación, ya que el encabezado es correcto."

        # Test case 2: encabezado del archivo CSV no es correcto
        header = ['id', 'first_name', 'last_name']
        try:
            validate_csv_header(header,good_header)
        except Exception as e:
            self.assertEqual(str(e),"El archivo CSV debe tener exactamente tres columnas con los nombres de columna 'id', 'firstname' y 'lastname', y en ese orden.")
            pass
    
    def test_import_customer_row(self):
        # Test case 1: importar una fila de cliente correcta
        row = ['123', 'John', 'Doe']
        with patch.object(Customer.objects, 'filter', return_value=Customer.objects.none()):
            with patch.object(Customer.objects, 'create', return_value=Mock(spec=Customer)) as mock_customer_create:
                import_customer_row(row)
                mock_customer_create.assert_called_once_with(id=123, first_name='John', last_name='Doe')

        # Test case 2: cliente con id ya existente en la base de datos
        row = ['123', 'Jane', 'Doe']
        with patch.object(Customer.objects, 'filter', return_value=Customer.objects.all()):
            try:
                import_customer_row(row)
                assert False, "Aquí el cliente ya existe en bbdd"
            except Exception as e:
                pass
                

        # Test case 3: error al importar el cliente
        row = ['123', 'Jane', 'Doe']
        with patch.object(Customer.objects, 'filter', return_value=Customer.objects.none()):
            with patch.object(Customer.objects, 'create', side_effect=Exception("Error al crear el objeto")):
                try:
                    import_customer_row(row)
                    assert False, "Error al importar el cliente."
                except Exception as e:
                    pass

class ImportProductTest(TestCase):
    def test_import_customer_row(self):
    # Test case 1: importar una fila de producto correcto
        row = ['1', 'mesa', 12.49]
        with patch.object(Product.objects, 'filter', return_value=Product.objects.none()):
            with patch.object(Product.objects, 'create', return_value=Mock(spec=Product)) as mock_product_create:
                import_product_row(row)
                mock_product_create.assert_called_once_with(id=1, name='mesa', cost=12.49)

        # Test case 2: Producto con id ya existente en la base de datos
        row = ['1', 'silla', 1.20]
        with patch.object(Product.objects, 'filter', return_value=Product.objects.all()):
            try:
                import_product_row(row)
                assert False, "Aquí el producto ya existe en bbdd"
            except Exception as e:
                pass