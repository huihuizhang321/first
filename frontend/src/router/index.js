import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
  { path: '/customers', name: 'customers', component: () => import('../views/CustomerView.vue') },
  { path: '/deals', name: 'deals', component: () => import('../views/DealView.vue') },
  { path: '/tasks', name: 'tasks', component: () => import('../views/TaskView.vue') },
  { path: '/contacts', name: 'contacts', component: () => import('../views/ContactView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
