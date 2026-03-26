<template>
  <div class="chat-panel-container">
    <div class="chat-header">
      <h3>AI 助手</h3>
      <el-button text size="small" @click="chatStore.clearHistory()">清空</el-button>
    </div>
    <ChatWindow />
  </div>
</template>

<script setup>
import { useChatStore } from '../../stores/chat'
import ChatWindow from '../chat/ChatWindow.vue'

const chatStore = useChatStore()
</script>

<style scoped>
.chat-panel-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
}

.chat-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>
