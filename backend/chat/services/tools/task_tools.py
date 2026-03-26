from crm.models import Task
from crm.serializers import TaskSerializer


def get_tools():
    return [
        (SEARCH_TASKS, handle_search_tasks),
        (CREATE_TASK, handle_create_task),
        (UPDATE_TASK, handle_update_task),
    ]


SEARCH_TASKS = {
    'name': 'search_tasks',
    'description': '搜索和筛选任务。可以按完成状态、优先级、客户、到期日期搜索。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'is_completed': {'type': 'boolean', 'description': '按完成状态筛选'},
            'priority': {'type': 'string', 'enum': ['low', 'medium', 'high']},
            'customer_id': {'type': 'integer', 'description': '按客户ID筛选'},
            'query': {'type': 'string', 'description': '按标题搜索'},
            'limit': {'type': 'integer', 'description': '最大返回数量，默认10'},
        },
        'required': [],
    },
}

CREATE_TASK = {
    'name': 'create_task',
    'description': '创建新任务，可以关联到客户或交易。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'title': {'type': 'string', 'description': '任务标题'},
            'description': {'type': 'string', 'description': '任务描述'},
            'customer': {'type': 'integer', 'description': '关联客户ID'},
            'deal': {'type': 'integer', 'description': '关联交易ID'},
            'due_date': {'type': 'string', 'description': '到期日期 (YYYY-MM-DD)'},
            'priority': {'type': 'string', 'enum': ['low', 'medium', 'high']},
        },
        'required': ['title'],
    },
}

UPDATE_TASK = {
    'name': 'update_task',
    'description': '更新任务，如标记完成、修改优先级等。',
    'input_schema': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'description': '任务ID'},
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'is_completed': {'type': 'boolean'},
            'priority': {'type': 'string', 'enum': ['low', 'medium', 'high']},
            'due_date': {'type': 'string', 'description': 'YYYY-MM-DD'},
        },
        'required': ['id'],
    },
}


def handle_search_tasks(input_data):
    qs = Task.objects.select_related('customer', 'deal').all()
    if 'is_completed' in input_data:
        qs = qs.filter(is_completed=input_data['is_completed'])
    if priority := input_data.get('priority'):
        qs = qs.filter(priority=priority)
    if customer_id := input_data.get('customer_id'):
        qs = qs.filter(customer_id=customer_id)
    if query := input_data.get('query'):
        qs = qs.filter(title__icontains=query)
    limit = input_data.get('limit', 10)
    data = TaskSerializer(qs[:limit], many=True).data

    crm_action = {
        'action': 'navigate',
        'target': 'tasks',
        'filters': {k: v for k, v in input_data.items() if k != 'limit'},
    }
    return data, crm_action


def handle_create_task(input_data):
    serializer = TaskSerializer(data=input_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'tasks'}
    return serializer.data, crm_action


def handle_update_task(input_data):
    task_id = input_data.pop('id')
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return {'error': f'任务ID {task_id} 不存在'}, None
    serializer = TaskSerializer(task, data=input_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    crm_action = {'action': 'refresh', 'target': 'tasks'}
    return serializer.data, crm_action
