<template>
  <div>
    <div class="toolbar">
      <el-input v-model="search" placeholder="搜索客户..." clearable style="width: 240px" @input="onSearch" />
      <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="fetchData" style="width: 140px; margin-left: 12px">
        <el-option label="潜在客户" value="prospect" />
        <el-option label="活跃" value="active" />
        <el-option label="不活跃" value="inactive" />
      </el-select>
    </div>
    <el-table :data="customers" v-loading="loading" stripe>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="company" label="公司" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="deals_count" label="交易数" width="80" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { customerApi } from '../../api/customers'
import { useCrmStore } from '../../stores/crm'

const crmStore = useCrmStore()
const customers = ref([])
const loading = ref(false)
const search = ref('')
const statusFilter = ref('')

const STATUS_MAP = { prospect: '潜在客户', active: '活跃', inactive: '不活跃' }
const TAG_TYPE_MAP = { prospect: 'warning', active: 'success', inactive: 'info' }

function statusLabel(s) { return STATUS_MAP[s] || s }
function statusTagType(s) { return TAG_TYPE_MAP[s] || '' }

async function fetchData() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    const { data } = await customerApi.list(params)
    customers.value = data.results || data
  } finally {
    loading.value = false
  }
}

function onSearch() {
  fetchData()
}

// React to AI-triggered navigation filters
watch(() => crmStore.filters, (filters) => {
  if (filters.query) search.value = filters.query
  if (filters.status) statusFilter.value = filters.status
  fetchData()
}, { deep: true })

// React to AI-triggered refresh
watch(() => crmStore.refreshTrigger, fetchData)

onMounted(() => {
  if (crmStore.filters.query) search.value = crmStore.filters.query
  if (crmStore.filters.status) statusFilter.value = crmStore.filters.status
  fetchData()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  margin-bottom: 16px;
}
</style>
