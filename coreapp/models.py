from django.core.exceptions import ValidationError
from django.db import models
from djmoney.models.fields import MoneyField


class Network(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


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
    network = models.ForeignKey(
        'coreapp.Network',
        related_name='unit_network',
        on_delete=models.CASCADE
    )
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
        default=0,
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def clean(self):
        # Hierarchy validation
        if self.provider and not int(self.unit_type) > int(self.provider.unit_type):
            raise ValidationError("Error in unit_type hierarchy. HINT: You can choose only the higher Unit as provider")

        # Single unit_type in network validation
        potential_matched_type_unit: Unit = Unit.objects.filter(
            network=self.network,
            unit_type=self.unit_type
        ).first()
        if potential_matched_type_unit and potential_matched_type_unit != self:
            raise ValidationError("Error in network structure. HINT: You can't add second unit of this type to this "
                                  "network")
