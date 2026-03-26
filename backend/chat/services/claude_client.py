import json
import os
import anthropic
from .tool_registry import TOOLS, execute_tool

client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY', ''))

SYSTEM_PROMPT = """你是一个CRM助手。你帮助用户管理客户、交易、任务和联系人。

使用提供的工具来读取和写入CRM数据。当你检索数据时，用自然语言描述结果。当你修改数据时，确认你所做的操作。

规则：
- 始终使用工具来获取真实数据，不要编造数据
- 用中文回复用户
- 保持回复简洁有用
- 当用户询问模糊的问题时，主动使用工具查找相关信息"""


def get_chat_response(user_message, history):
    """Generator that yields SSE events during the AI chat loop."""
    messages = []
    for msg in history:
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': user_message})

    while True:
        try:
            response = client.messages.create(
                model='claude-sonnet-4-20250514',
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )
        except anthropic.APIError as e:
            yield {'type': 'error', 'message': f'AI服务错误: {str(e)}'}
            yield {'type': 'done'}
            return

        # Process each content block
        for block in response.content:
            if block.type == 'text':
                yield {'type': 'text', 'content': block.text}
            elif block.type == 'tool_use':
                yield {'type': 'tool_call', 'tool': block.name, 'input': block.input}

                result, crm_action = execute_tool(block.name, block.input)
                yield {'type': 'tool_result', 'tool': block.name, 'data': result}

                if crm_action:
                    yield {'type': 'crm_action', **crm_action}

        # If the model wants to use tools, feed the results back and loop
        if response.stop_reason == 'tool_use':
            # Append the full assistant message
            messages.append({'role': 'assistant', 'content': response.content})

            # Build tool results for all tool_use blocks
            tool_results = []
            for block in response.content:
                if block.type == 'tool_use':
                    result, _ = execute_tool(block.name, block.input)
                    tool_results.append({
                        'type': 'tool_result',
                        'tool_use_id': block.id,
                        'content': json.dumps(result, ensure_ascii=False, default=str),
                    })
            messages.append({'role': 'user', 'content': tool_results})
            continue

        # end_turn or other stop reasons — we're done
        break

    yield {'type': 'done'}
