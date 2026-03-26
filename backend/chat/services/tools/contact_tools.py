from crm.models import Contact
from crm.serializers import ContactSerializer


def get_tools():
    return [
        (SEARCH_CONTACTS, handle_search_contacts),
        (CREATE_CONTACT, handle_create_contact),
    ]


SEARCH_CONTACTS = {
    'name': 'search_contacts',
    'description': '搜索联系人。可以按客户ID或名称搜索。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'customer_id': {'type': 'integer', 'description': '按客户ID筛选'},
            'query': {'type': 'string', 'description': '按名称搜索'},
            'limit': {'type': 'integer', 'description': '最大返回数量，默认10'},
        },
        'required': [],
    },
}

CREATE_CONTACT = {
    'name': 'create_contact',
    'description': '为客户添加新联系人。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'customer': {'type': 'integer', 'description': '所属客户ID'},
            'name': {'type': 'string', 'description': '联系人名称'},
            'role': {'type': 'string', 'description': '职位角色'},
            'email': {'type': 'string'},
            'phone': {'type': 'string'},
            'is_primary': {'type': 'boolean', 'description': '是否为主要联系人'},
        },
        'required': ['customer', 'name'],
    },
}


def handle_search_contacts(input_data):
    qs = Contact.objects.select_related('customer').all()
    if customer_id := input_data.get('customer_id'):
        qs = qs.filter(customer_id=customer_id)
    if query := input_data.get('query'):
        qs = qs.filter(name__icontains=query)
    limit = input_data.get('limit', 10)
    data = ContactSerializer(qs[:limit], many=True).data

    crm_action = {
        'action': 'navigate',
        'target': 'contacts',
        'filters': {k: v for k, v in input_data.items() if k != 'limit'},
    }
    return data, crm_action


def handle_create_contact(input_data):
    serializer = ContactSerializer(data=input_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'contacts'}
    return serializer.data, crm_action
