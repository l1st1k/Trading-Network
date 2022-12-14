# Generated by Django 4.1.3 on 2022-11-11 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=30)),
                ('house_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('model', models.CharField(max_length=30)),
                ('release_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('email', models.EmailField(max_length=50)),
                ('unit_type', models.IntegerField(choices=[('0', 'Factory'), ('1', 'Distributor'), ('2', 'Dealership'), ('3', 'Large Retail Chain'), ('4', 'Individual Entrepreneur')], default='0')),
                ('debt_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True)),
                ('debt', djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='USD', max_digits=14, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='coreapp.address')),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(blank=True, related_name='products', to='coreapp.product')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_provider', to='coreapp.unit')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
    ]
