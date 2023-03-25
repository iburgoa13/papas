from django.db import models

# Create your models here.

class Customers(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(null=False, default="sin correo")