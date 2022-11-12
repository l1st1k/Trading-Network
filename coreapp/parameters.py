from drf_yasg import openapi

network_id_parameter = openapi.Parameter(
    'network_id',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER
)

country_parameter = openapi.Parameter(
    'country',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING
)

product_id_parameter = openapi.Parameter(
    'product_id',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_INTEGER
)

high_debt_parameter = openapi.Parameter(
    'high_debt',
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_BOOLEAN
)
