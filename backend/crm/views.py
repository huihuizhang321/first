from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Contact, Deal, Task
from .serializers import CustomerSerializer, ContactSerializer, DealSerializer, TaskSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['status']
    search_fields = ['name', 'company', 'email']
    ordering_fields = ['name', 'created_at', 'updated_at']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.select_related('customer').all()
    serializer_class = ContactSerializer
    filterset_fields = ['customer', 'is_primary']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related('customer').all()
    serializer_class = DealSerializer
    filterset_fields = ['stage', 'customer']
    search_fields = ['title']
    ordering_fields = ['value', 'expected_close', 'created_at']


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('customer', 'deal').all()
    serializer_class = TaskSerializer
    filterset_fields = ['is_completed', 'priority', 'customer', 'deal']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']
