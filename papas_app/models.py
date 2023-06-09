from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Customer(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0.0)])

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    id_order = models.IntegerField(default=-1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    class Meta:
        unique_together = ('id_order','customer','product')
    def __str__(self):
        return f"Order {self.id} for {self.customer}"