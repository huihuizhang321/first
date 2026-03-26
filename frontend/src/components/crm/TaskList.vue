<template>
  <div>
    <div class="toolbar">
      <el-input v-model="search" placeholder="搜索任务..." clearable style="width: 240px" @input="fetchData" />
      <el-select v-model="priorityFilter" placeholder="优先级" clearable @change="fetchData" style="width: 120px; margin-left: 12px">
        <el-option label="高" value="high" />
        <el-option label="中" value="medium" />
        <el-option label="低" value="low" />
      </el-select>
      <el-checkbox v-model="hideCompleted" label="隐藏已完成" style="margin-left: 12px" @change="fetchData" />
    </div>
    <el-table :data="tasks" v-loading="loading" stripe>
      <el-table-column prop="title" label="任务" />
      <el-table-column prop="customer_name" label="客户" width="120" />
      <el-table-column prop="priority" label="优先级" width="80">
        <template #default="{ row }">
          <el-tag :type="priorityTagType(row.priority)" size="small">{{ priorityLabel(row.priority) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="due_date" label="到期日" width="110" />
      <el-table-column prop="is_completed" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_completed ? 'success' : 'info'" size="small">
            {{ row.is_completed ? '已完成' : '进行中' }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { taskApi } from '../../api/tasks'
import { useCrmStore } from '../../stores/crm'

const crmStore = useCrmStore()
const tasks = ref([])
const loading = ref(false)
const search = ref('')
const priorityFilter = ref('')
const hideCompleted = ref(true)

const PRIORITY_MAP = { high: '高', medium: '中', low: '低' }
const PRIORITY_TAG = { high: 'danger', medium: 'warning', low: 'info' }

function priorityLabel(p) { return PRIORITY_MAP[p] || p }
function priorityTagType(p) { return PRIORITY_TAG[p] || '' }

async function fetchData() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (priorityFilter.value) params.priority = priorityFilter.value
    if (hideCompleted.value) params.is_completed = false
    const { data } = await taskApi.list(params)
    tasks.value = data.results || data
  } finally {
    loading.value = false
  }
}

watch(() => crmStore.filters, (filters) => {
  if (filters.priority) priorityFilter.value = filters.priority
  if (filters.query) search.value = filters.query
  if ('is_completed' in filters) hideCompleted.value = !filters.is_completed
  fetchData()
}, { deep: true })

watch(() => crmStore.refreshTrigger, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.toolbar { display: flex; align-items: center; margin-bottom: 16px; }
</style>
