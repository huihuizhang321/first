<template>
  <div class="chat-window">
    <div class="messages" ref="messagesRef">
      <div v-if="chatStore.messages.length === 0" class="empty-hint">
        <p>你好！我是你的CRM助手。</p>
        <p>试试问我：</p>
        <ul>
          <li>"展示所有客户"</li>
          <li>"有哪些正在洽谈的交易？"</li>
          <li>"创建一个新任务"</li>
        </ul>
      </div>
      <ChatMessage
        v-for="(msg, index) in chatStore.messages"
        :key="index"
        :message="msg"
      />
      <div v-if="chatStore.isStreaming" class="typing-indicator">
        <span></span><span></span><span></span>
      </div>
    </div>
    <ChatInput @send="onSend" :disabled="chatStore.isStreaming" />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatStore } from '../../stores/chat'
import ChatMessage from './ChatMessage.vue'
import ChatInput from './ChatInput.vue'

const chatStore = useChatStore()
const messagesRef = ref(null)

// Auto-scroll to bottom on new messages
watch(
  () => chatStore.messages.length,
  async () => {
    await nextTick()
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  }
)

function onSend(text) {
  chatStore.sendMessage(text)
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.empty-hint {
  color: #909399;
  font-size: 14px;
  line-height: 1.8;
  padding: 20px 0;
}

.empty-hint ul {
  margin-top: 8px;
  padding-left: 20px;
}

.empty-hint li {
  cursor: pointer;
  color: #409eff;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #c0c4cc;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
