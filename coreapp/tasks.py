from random import randint
from typing import Callable

from asgiref.sync import async_to_sync
from celery import shared_task
from django.db import transaction
from djmoney.money import Money
from TradingNetwork.celery import app

from coreapp.models import Unit


@shared_task
def celery_raise_debt():
    queryset = Unit.objects.all()
    for unit in queryset:
        random_int: int = randint(5, 500)
        debt_currency = unit.debt_currency
        unit.debt += Money(random_int, currency=debt_currency)
        unit.save()


@shared_task
def celery_reduce_debt():
    queryset = Unit.objects.all()
    for unit in queryset:
        random_int: int = randint(100, 10000)
        debt_currency = unit.debt_currency
        unit.debt -= Money(random_int, currency=debt_currency)
        if unit.debt < Money(0, currency=debt_currency):
            unit.debt = 0
        unit.save()


@app.task(ignore_result=True)
def celery_remove_debt(ids: list[int]):
    with transaction.atomic():
        Unit.objects.filter(pk__in=ids).update(debt=0)
