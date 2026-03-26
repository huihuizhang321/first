from rest_framework import serializers
from .models import Customer, Contact, Deal, Task


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Deal
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True, default=None)
    deal_title = serializers.CharField(source='deal.title', read_only=True, default=None)

    class Meta:
        model = Task
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    contacts_count = serializers.IntegerField(source='contacts.count', read_only=True)
    deals_count = serializers.IntegerField(source='deals.count', read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
