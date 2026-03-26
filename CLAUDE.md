# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A web-based AI-powered CRM demo. Left panel: AI chat interface. Right panel: CRM workspace (customers, deals, tasks, contacts). The AI chat accepts natural language queries, reads/writes CRM data via Claude tool use, and all CRM operations are completable through conversation.

## Tech Stack

- **Frontend**: Vue 3 + Vite + Element Plus + Pinia
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: MySQL
- **AI**: Claude API via `anthropic` Python SDK (tool use for CRM data operations)

## Development Commands

### Backend
```bash
cd backend
pip install -r requirements.txt          # Install dependencies
python manage.py migrate                 # Run migrations
python manage.py seed_crm                # Seed sample data
python manage.py runserver               # Start dev server (port 8000)
```

### Frontend
```bash
cd frontend
npm install                              # Install dependencies
npm run dev                              # Start dev server (port 3000, proxies /api → :8000)
npm run build                            # Production build
```

### Environment Variables
- `ANTHROPIC_API_KEY` — required for AI chat
- `DB_NAME` (default: `ai_crm`), `DB_USER` (default: `root`), `DB_PASSWORD`, `DB_HOST` (default: `127.0.0.1`), `DB_PORT` (default: `3306`)

## Architecture

### Backend Structure
- `config/` — Django project settings, root URLs
- `crm/` — CRM data app: models (Customer, Contact, Deal, Task), DRF viewsets, serializers. All REST endpoints under `/api/crm/`
- `chat/` — AI chat app: SSE endpoint at `POST /api/chat/`
  - `services/claude_client.py` — Core AI integration: system prompt, tool-use loop, SSE event generation
  - `services/tool_registry.py` — Auto-collects tools from sub-modules, dispatches tool calls
  - `services/tools/` — One file per entity (customer_tools.py, deal_tools.py, etc.), each exports `get_tools()` returning `(definition, handler)` tuples

### Frontend Structure
- `components/layout/` — AppLayout (split panel), ChatPanel, MainPanel (nav + router-view)
- `components/chat/` — ChatWindow, ChatMessage, ChatInput
- `components/crm/` — CustomerList, DealList, TaskList, ContactList (Element Plus tables)
- `stores/chat.js` — Chat messages, SSE streaming, dispatches `crm_action` events to crm store
- `stores/crm.js` — Active view state, filters, `handleAction()` bridges AI actions to router navigation
- `api/chat.js` — SSE client using `fetch` + `ReadableStream` async generator (not axios)
- `api/*.js` — Axios-based CRUD wrappers per entity

### Key Integration Pattern: Chat → CRM Bridge
1. User sends message → `chatStore.sendMessage()` → `POST /api/chat/` (SSE)
2. Backend runs Claude tool-use loop, emits SSE events: `text`, `tool_call`, `tool_result`, `crm_action`, `done`
3. `crm_action` events carry `{action: "navigate"|"refresh", target, filters}`
4. Frontend `chatStore` receives `crm_action` → calls `crmStore.handleAction()` → pushes router navigation
5. CRM list components watch `crmStore.filters` and `refreshTrigger` to re-fetch data

### Extensibility: Adding a New CRM Entity
1. Add model to `backend/crm/models.py`
2. Add serializer to `backend/crm/serializers.py`
3. Add viewset to `backend/crm/views.py`, register in `crm/urls.py` router
4. Create `backend/chat/services/tools/<entity>_tools.py` with `get_tools()`
5. Import in `tool_registry.py`'s `_TOOL_MODULES` list
6. Add frontend: API module, list component, view, route
