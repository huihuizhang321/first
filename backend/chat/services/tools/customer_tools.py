from crm.models import Customer
from crm.serializers import CustomerSerializer


def get_tools():
    return [
        (SEARCH_CUSTOMERS, handle_search_customers),
        (CREATE_CUSTOMER, handle_create_customer),
        (UPDATE_CUSTOMER, handle_update_customer),
    ]


SEARCH_CUSTOMERS = {
    'name': 'search_customers',
    'description': '搜索和筛选客户。可以按名称、公司、状态搜索，或列出最近的客户。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'query': {'type': 'string', 'description': '按名称或公司搜索'},
            'status': {'type': 'string', 'enum': ['prospect', 'active', 'inactive'], 'description': '按状态筛选'},
            'limit': {'type': 'integer', 'description': '最大返回数量，默认10'},
        },
        'required': [],
    },
}

CREATE_CUSTOMER = {
    'name': 'create_customer',
    'description': '创建新客户记录。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'name': {'type': 'string', 'description': '客户名称'},
            'company': {'type': 'string', 'description': '公司名称'},
            'email': {'type': 'string', 'description': '邮箱'},
            'phone': {'type': 'string', 'description': '电话'},
            'status': {'type': 'string', 'enum': ['prospect', 'active', 'inactive'], 'description': '客户状态'},
            'notes': {'type': 'string', 'description': '备注'},
        },
        'required': ['name'],
    },
}

UPDATE_CUSTOMER = {
    'name': 'update_customer',
    'description': '更新现有客户的信息。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'description': '客户ID'},
            'name': {'type': 'string'},
            'company': {'type': 'string'},
            'email': {'type': 'string'},
            'phone': {'type': 'string'},
            'status': {'type': 'string', 'enum': ['prospect', 'active', 'inactive']},
            'notes': {'type': 'string'},
        },
        'required': ['id'],
    },
}


def handle_search_customers(input_data):
    qs = Customer.objects.all()
    if query := input_data.get('query'):
        from django.db.models import Q
        qs = qs.filter(Q(name__icontains=query) | Q(company__icontains=query))
    if status := input_data.get('status'):
        qs = qs.filter(status=status)
    limit = input_data.get('limit', 10)
    qs = qs[:limit]
    data = CustomerSerializer(qs, many=True).data

    crm_action = {
        'action': 'navigate',
        'target': 'customers',
        'filters': {k: v for k, v in input_data.items() if k != 'limit'},
    }
    return data, crm_action


def handle_create_customer(input_data):
    serializer = CustomerSerializer(data=input_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'customers'}
    return serializer.data, crm_action


def handle_update_customer(input_data):
    customer_id = input_data.pop('id')
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return {'error': f'客户ID {customer_id} 不存在'}, None
    serializer = CustomerSerializer(customer, data=input_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'customers'}
    return serializer.data, crm_action
