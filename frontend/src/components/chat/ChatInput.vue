<template>
  <div class="chat-input">
    <el-input
      v-model="text"
      :placeholder="disabled ? 'AI正在思考...' : '输入消息...'"
      :disabled="disabled"
      @keydown.enter.exact.prevent="send"
      clearable
    >
      <template #append>
        <el-button :icon="Promotion" :disabled="disabled || !text.trim()" @click="send" />
      </template>
    </el-input>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Promotion } from '@element-plus/icons-vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(['send'])
const text = ref('')

function send() {
  if (!text.value.trim() || props.disabled) return
  emit('send', text.value.trim())
  text.value = ''
}
</script>

<style scoped>
.chat-input {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  background: white;
}
</style>
