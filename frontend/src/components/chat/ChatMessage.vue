<template>
  <div class="chat-message" :class="message.role">
    <div class="bubble">
      <div class="content">{{ message.content }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: { type: Object, required: true },
})
</script>

<style scoped>
.chat-message {
  margin-bottom: 12px;
  display: flex;
}

.chat-message.user {
  justify-content: flex-end;
}

.chat-message.assistant {
  justify-content: flex-start;
}

.chat-message.system {
  justify-content: center;
}

.bubble {
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
}

.user .bubble {
  background: #409eff;
  color: white;
  border-bottom-right-radius: 4px;
}

.assistant .bubble {
  background: white;
  color: #303133;
  border: 1px solid #e4e7ed;
  border-bottom-left-radius: 4px;
}

.system .bubble {
  background: transparent;
  color: #909399;
  font-size: 12px;
  padding: 4px 8px;
}
</style>
