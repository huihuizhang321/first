<template>
  <div>
    <div class="toolbar">
      <el-input v-model="search" placeholder="搜索联系人..." clearable style="width: 240px" @input="fetchData" />
    </div>
    <el-table :data="contacts" v-loading="loading" stripe>
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="role" label="职位" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="is_primary" label="主要联系人" width="100">
        <template #default="{ row }">
          <el-tag v-if="row.is_primary" type="success" size="small">是</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { contactApi } from '../../api/contacts'
import { useCrmStore } from '../../stores/crm'

const crmStore = useCrmStore()
const contacts = ref([])
const loading = ref(false)
const search = ref('')

async function fetchData() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (crmStore.filters.customer_id) params.customer = crmStore.filters.customer_id
    const { data } = await contactApi.list(params)
    contacts.value = data.results || data
  } finally {
    loading.value = false
  }
}

watch(() => crmStore.filters, () => fetchData(), { deep: true })
watch(() => crmStore.refreshTrigger, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.toolbar { display: flex; margin-bottom: 16px; }
</style>
