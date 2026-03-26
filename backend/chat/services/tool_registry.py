from .tools import customer_tools, contact_tools, deal_tools, task_tools

_TOOL_MODULES = [
    customer_tools,
    contact_tools,
    deal_tools,
    task_tools,
]

TOOLS = []
_HANDLERS = {}

for _module in _TOOL_MODULES:
    for tool_def, handler_fn in _module.get_tools():
        TOOLS.append(tool_def)
        _HANDLERS[tool_def['name']] = handler_fn


def execute_tool(name, input_data):
    """Execute a tool by name. Returns (result_data, optional_crm_action)."""
    handler = _HANDLERS.get(name)
    if not handler:
        return {'error': f'Unknown tool: {name}'}, None
    return handler(input_data)
