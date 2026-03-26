<template>
  <div class="app-layout">
    <ChatPanel class="chat-panel" />
    <MainPanel class="main-panel" />
  </div>
</template>

<script setup>
import ChatPanel from './ChatPanel.vue'
import MainPanel from './MainPanel.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.chat-panel {
  width: 380px;
  min-width: 380px;
  border-right: 1px solid #e4e7ed;
  background: #fafafa;
}

.main-panel {
  flex: 1;
  overflow: hidden;
}
</style>
