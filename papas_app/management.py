from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from papas_app.views import import_customers
import csv

class Command(BaseCommand):
    help = 'Importa clientes desde un archivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help='Ruta del archivo CSV a importar')

    def handle(self, *args, **options):
        file_path = options['file_path']

        # Creamos un objeto RequestFactory para poder pasar un objeto `request`
        # a la función `import_customers_from_csv()`.
        request_factory = RequestFactory()
        request = request_factory.get('prueba/')

        try:
            # Llamamos a la función `import_customers_from_csv()` y le pasamos el objeto `request`.
            import_customers(request, file_path)
            self.stdout.write(self.style.SUCCESS('Clientes importados con éxito.'))
        except Exception as e:
            self.stderr.write(str(e))
            self.stderr.write(self.style.ERROR('Error al importar clientes.'))