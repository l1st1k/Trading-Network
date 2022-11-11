from djmoney.models.fields import MoneyField
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    model = models.CharField(max_length=30)
    release_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.IntegerField()

    def __str__(self):
        return self.city + ', ' + self.street + ', ' + str(self.house_number)


class Unit(models.Model):
    class UnitType(models.TextChoices):
        FACTORY = 0
        DISTRIBUTOR = 1
        DEALERSHIP = 2
        LARGE_RETAIL_CHAIN = 3
        INDIVIDUAL_ENTREPRENEUR = 4

    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=50)
    address = models.ForeignKey(
        'coreapp.Address',
        related_name='address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    provider = models.ForeignKey(
        'coreapp.Unit',
        related_name='unit_provider',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    products = models.ManyToManyField(
        'coreapp.Product',
        related_name='products',
        blank=True
    )
    members = models.ManyToManyField(
        'User.User',
        related_name='members',
        blank=True
    )
    unit_type = models.CharField(
        max_length=2,
        choices=UnitType.choices,
        default=UnitType.FACTORY
    )
    debt = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
