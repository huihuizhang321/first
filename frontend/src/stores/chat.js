import { defineStore } from 'pinia'
import { chatStream } from '../api/chat'
import { useCrmStore } from './crm'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [],
    isStreaming: false,
  }),

  actions: {
    async sendMessage(text) {
      if (!text.trim() || this.isStreaming) return

      this.messages.push({
        role: 'user',
        content: text,
        timestamp: new Date().toISOString(),
      })

      this.isStreaming = true
      const crmStore = useCrmStore()
      let assistantContent = ''

      // Build history for the API (exclude timestamps)
      const history = this.messages.slice(0, -1)
        .filter(m => m.role === 'user' || m.role === 'assistant')
        .map(m => ({ role: m.role, content: m.content }))

      try {
        for await (const event of chatStream(text, history)) {
          switch (event.type) {
            case 'text':
              assistantContent += event.content
              // Update the last assistant message reactively
              this._updateAssistantMessage(assistantContent)
              break
            case 'tool_call':
              this._addSystemMessage(`正在调用: ${event.tool}`)
              break
            case 'crm_action':
              crmStore.handleAction(event)
              break
            case 'error':
              this._addSystemMessage(`错误: ${event.message}`)
              break
            case 'done':
              break
          }
        }
      } catch (err) {
        this._addSystemMessage(`连接错误: ${err.message}`)
      }

      // Finalize assistant message
      if (assistantContent) {
        this._finalizeAssistantMessage(assistantContent)
      }
      this.isStreaming = false
    },

    _updateAssistantMessage(content) {
      const last = this.messages[this.messages.length - 1]
      if (last && last.role === 'assistant' && last._streaming) {
        last.content = content
      } else {
        this.messages.push({
          role: 'assistant',
          content,
          timestamp: new Date().toISOString(),
          _streaming: true,
        })
      }
    },

    _finalizeAssistantMessage(content) {
      const last = this.messages[this.messages.length - 1]
      if (last && last._streaming) {
        last.content = content
        delete last._streaming
      }
    },

    _addSystemMessage(content) {
      this.messages.push({
        role: 'system',
        content,
        timestamp: new Date().toISOString(),
      })
    },

    clearHistory() {
      this.messages = []
    },
  },
})
