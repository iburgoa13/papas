# Generated by Django 4.1.7 on 2023-03-26 16:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papas_app.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papas_app.product')),
            ],
        ),
    ]
