<template>
  <div class="main-panel-container">
    <div class="nav-bar">
      <el-menu mode="horizontal" :default-active="route.name" @select="onMenuSelect">
        <el-menu-item index="dashboard">仪表盘</el-menu-item>
        <el-menu-item index="customers">客户</el-menu-item>
        <el-menu-item index="deals">交易</el-menu-item>
        <el-menu-item index="tasks">任务</el-menu-item>
        <el-menu-item index="contacts">联系人</el-menu-item>
      </el-menu>
    </div>
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useCrmStore } from '../../stores/crm'

const route = useRoute()
const crmStore = useCrmStore()

function onMenuSelect(name) {
  crmStore.navigate(name)
}
</script>

<style scoped>
.main-panel-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.nav-bar {
  border-bottom: 1px solid #e4e7ed;
}

.content-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
