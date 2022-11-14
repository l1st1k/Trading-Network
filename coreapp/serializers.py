from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from coreapp.models import *


class NetworkSerializer(serializers.ModelSerializer):
    unit_amount = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = ('id', 'name', 'unit_amount', 'units')

    def get_unit_amount(self, obj):
        return Unit.objects.filter(network=obj).count()

    def get_units(self, obj):
        units = Unit.objects.filter(network=obj).order_by('unit_type')
        return UnitShortSerializer(units, many=True).data


class NetworkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class UnitNoDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = ('debt', 'debt_currency')


class UnitShortSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'unit_type', 'provider')

    def get_provider(self, obj):
        return obj.provider.name if obj.provider else None


class ProductSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the release_date is after the current time.
        """
        # Added 3h manually, because TZ from setting.py doesn't work right
        now = timezone.now() + timedelta(hours=3)
        if not data['release_date'] > now:
            raise serializers.ValidationError("Incorrect release_date! release_date should be future.")
        return data

    class Meta:
        model = Product
        fields = '__all__'
