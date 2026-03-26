from crm.models import Deal
from crm.serializers import DealSerializer


def get_tools():
    return [
        (SEARCH_DEALS, handle_search_deals),
        (CREATE_DEAL, handle_create_deal),
        (UPDATE_DEAL, handle_update_deal),
    ]


SEARCH_DEALS = {
    'name': 'search_deals',
    'description': '搜索和筛选交易。可以按阶段、客户、金额范围搜索。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'stage': {'type': 'string', 'enum': ['qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost']},
            'customer_id': {'type': 'integer', 'description': '按客户ID筛选'},
            'query': {'type': 'string', 'description': '按标题搜索'},
            'limit': {'type': 'integer', 'description': '最大返回数量，默认10'},
        },
        'required': [],
    },
}

CREATE_DEAL = {
    'name': 'create_deal',
    'description': '创建新交易。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'customer': {'type': 'integer', 'description': '所属客户ID'},
            'title': {'type': 'string', 'description': '交易标题'},
            'value': {'type': 'number', 'description': '交易金额'},
            'stage': {'type': 'string', 'enum': ['qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost']},
            'expected_close': {'type': 'string', 'description': '预计成交日期 (YYYY-MM-DD)'},
        },
        'required': ['customer', 'title'],
    },
}

UPDATE_DEAL = {
    'name': 'update_deal',
    'description': '更新交易信息，如阶段、金额等。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'description': '交易ID'},
            'title': {'type': 'string'},
            'value': {'type': 'number'},
            'stage': {'type': 'string', 'enum': ['qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost']},
            'expected_close': {'type': 'string', 'description': 'YYYY-MM-DD'},
        },
        'required': ['id'],
    },
}


def handle_search_deals(input_data):
    qs = Deal.objects.select_related('customer').all()
    if stage := input_data.get('stage'):
        qs = qs.filter(stage=stage)
    if customer_id := input_data.get('customer_id'):
        qs = qs.filter(customer_id=customer_id)
    if query := input_data.get('query'):
        qs = qs.filter(title__icontains=query)
    limit = input_data.get('limit', 10)
    data = DealSerializer(qs[:limit], many=True).data

    crm_action = {
        'action': 'navigate',
        'target': 'deals',
        'filters': {k: v for k, v in input_data.items() if k != 'limit'},
    }
    return data, crm_action


def handle_create_deal(input_data):
    serializer = DealSerializer(data=input_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'deals'}
    return serializer.data, crm_action


def handle_update_deal(input_data):
    deal_id = input_data.pop('id')
    try:
        deal = Deal.objects.get(id=deal_id)
    except Deal.DoesNotExist:
        return {'error': f'交易ID {deal_id} 不存在'}, None
    serializer = DealSerializer(deal, data=input_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'deals'}
    return serializer.data, crm_action
