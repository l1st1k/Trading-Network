import boto3
import qrcode
from django.db.models.query import QuerySet
from dotenv import dotenv_values

from coreapp.models import Product, Unit

config = dotenv_values("/usr/src/app/.env")
SES_ENDPOINT = config["SES_ENDPOINT"]
AWS_ACCESS_KEY = config["AWS_ACCESS_KEY"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
MAIL_SENDER = config["SES_MAIL_SENDER"]
AWS_REGION_NAME = config["AWS_REGION_NAME"]


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


def make_qr_code_for_unit(data) -> str:
    img = qrcode.make(data)
    path: str = 'temp_pict.png'
    img.save(path)
    return path


def create_and_send_qr_to_email(email: str, data):
    path = make_qr_code_for_unit(data=data)
    html_email_content = \
        f"""
            <html>
                <img src={path}>
            </html>
        """
    ses = boto3.client("ses",
                       endpoint_url=SES_ENDPOINT,
                       aws_access_key_id=AWS_ACCESS_KEY,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       region_name=AWS_REGION_NAME)
    ses.verify_email_identity(EmailAddress=MAIL_SENDER)
    ses.send_email(
        Destination={
            "ToAddresses": [email, ]
        },
        Message={
            "Body": {
                'Html': {
                    'Data': html_email_content,
                    'Charset': "UTF-8"
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "QR-code with unit contacts!",
            },
        },
        Source=MAIL_SENDER
    )
    # TODO fix SES client connection
    # http://localhost.localstack.cloud:4566/
