from django.db.models.query import QuerySet

from coreapp.models import Product, Unit


def filtering_unit_queryset(
        request,
        queryset
) -> 'QuerySet[Unit]':

    # Filter for certain network
    if request.GET.get('network_id', None):
        queryset = queryset.filter(network__id=request.GET['network_id'])

    # Filter for country
    if request.GET.get('country', None):
        queryset = queryset.filter(address__country=request.GET['country'])

    # Filter for product availability
    if request.GET.get('product_id', None):
        product = Product.objects.filter(pk=request.GET['product_id'])
        queryset = queryset.filter(products__in=product)

    # Filter for units with high debt
    if request.GET.get('high_debt', None):
        sum_of_debts = sum(Unit.objects.values_list('debt', flat=True))
        average_debt = sum_of_debts / queryset.count()
        queryset = queryset.filter(debt__gt=average_debt)

    return queryset
