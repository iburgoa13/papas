from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from papas_app.models import Customer

class ImportCustomersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.import_customers_url = reverse('import_customers')

    def test_import_customers_view_get(self):
        response = self.client.get(self.import_customers_url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'import_customers.html')

    def test_import_customers_view_post_wrong_file(self):
        csv_file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        response = self.client.post(self.import_customers_url, {'csv_file': csv_file})
        self.assertContains(response, 'El archivo seleccionado no es un archivo CSV.')

    def test_import_customers_view_post_success(self):
        csv_file = SimpleUploadedFile("file.csv", b"id,first_name,last_name\n1,John,Doe\n2,Jane,Doe\n", content_type="text/csv")
        response = self.client.post(self.import_customers_url, {'csv_file': csv_file})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_list'))
        self.assertEqual(len(Customer.objects.all()), 2)

    def test_import_customers_view_post_error(self):
        Customer.objects.create(id=1, first_name='John', last_name='Doe')
        csv_file = SimpleUploadedFile("file.csv", b"id,first_name,last_name\n1,John,Doe\n2,Jane,Doe\n", content_type="text/csv")
        response = self.client.post(self.import_customers_url, {'csv_file': csv_file})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'El cliente con id 1 ya existe')
        self.assertEqual(len(Customer.objects.all()), 1)