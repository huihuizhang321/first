<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6" v-for="card in cards" :key="card.label">
        <el-card shadow="hover" class="stat-card" @click="crmStore.navigate(card.route)">
          <div class="stat-value">{{ card.value }}</div>
          <div class="stat-label">{{ card.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCrmStore } from '../stores/crm'
import http from '../api/index'

const crmStore = useCrmStore()

const cards = ref([
  { label: '客户总数', value: '-', route: 'customers' },
  { label: '进行中交易', value: '-', route: 'deals' },
  { label: '待办任务', value: '-', route: 'tasks' },
  { label: '联系人', value: '-', route: 'contacts' },
])

onMounted(async () => {
  try {
    const [customers, deals, tasks, contacts] = await Promise.all([
      http.get('/crm/customers/'),
      http.get('/crm/deals/', { params: { stage: 'negotiation' } }),
      http.get('/crm/tasks/', { params: { is_completed: false } }),
      http.get('/crm/contacts/'),
    ])
    const count = (resp) => resp.data.count ?? (resp.data.results || resp.data).length
    cards.value[0].value = count(customers)
    cards.value[1].value = count(deals)
    cards.value[2].value = count(tasks)
    cards.value[3].value = count(contacts)
  } catch {
    // API not available yet
  }
})
</script>

<style scoped>
.stat-card {
  cursor: pointer;
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #409eff;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}
</style>
