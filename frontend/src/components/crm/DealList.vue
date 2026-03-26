<template>
  <div>
    <div class="toolbar">
      <el-input v-model="search" placeholder="搜索交易..." clearable style="width: 240px" @input="fetchData" />
      <el-select v-model="stageFilter" placeholder="阶段筛选" clearable @change="fetchData" style="width: 140px; margin-left: 12px">
        <el-option v-for="s in stages" :key="s.value" :label="s.label" :value="s.value" />
      </el-select>
    </div>
    <el-table :data="deals" v-loading="loading" stripe>
      <el-table-column prop="title" label="交易" />
      <el-table-column prop="customer_name" label="客户" />
      <el-table-column prop="value" label="金额" width="120">
        <template #default="{ row }">¥{{ Number(row.value).toLocaleString() }}</template>
      </el-table-column>
      <el-table-column prop="stage" label="阶段" width="120">
        <template #default="{ row }">
          <el-tag :type="stageTagType(row.stage)" size="small">{{ stageLabel(row.stage) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="expected_close" label="预计成交" width="120" />
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { dealApi } from '../../api/deals'
import { useCrmStore } from '../../stores/crm'

const crmStore = useCrmStore()
const deals = ref([])
const loading = ref(false)
const search = ref('')
const stageFilter = ref('')

const stages = [
  { value: 'qualification', label: '资格审查' },
  { value: 'proposal', label: '方案阶段' },
  { value: 'negotiation', label: '谈判中' },
  { value: 'closed_won', label: '已成交' },
  { value: 'closed_lost', label: '已流失' },
]

const STAGE_MAP = Object.fromEntries(stages.map(s => [s.value, s.label]))
const TAG_MAP = { qualification: 'info', proposal: 'warning', negotiation: '', closed_won: 'success', closed_lost: 'danger' }

function stageLabel(s) { return STAGE_MAP[s] || s }
function stageTagType(s) { return TAG_MAP[s] || '' }

async function fetchData() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (stageFilter.value) params.stage = stageFilter.value
    const { data } = await dealApi.list(params)
    deals.value = data.results || data
  } finally {
    loading.value = false
  }
}

watch(() => crmStore.filters, (filters) => {
  if (filters.stage) stageFilter.value = filters.stage
  if (filters.query) search.value = filters.query
  fetchData()
}, { deep: true })

watch(() => crmStore.refreshTrigger, fetchData)

onMounted(() => {
  if (crmStore.filters.stage) stageFilter.value = crmStore.filters.stage
  fetchData()
})
</script>

<style scoped>
.toolbar { display: flex; margin-bottom: 16px; }
</style>
