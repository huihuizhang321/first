import { defineStore } from 'pinia'
import router from '../router'

export const useCrmStore = defineStore('crm', {
  state: () => ({
    activeView: 'dashboard',
    filters: {},
    refreshTrigger: 0,
  }),

  actions: {
    handleAction(event) {
      if (event.action === 'navigate') {
        this.activeView = event.target
        this.filters = event.filters || {}
        router.push({ name: event.target, query: event.filters })
      } else if (event.action === 'refresh') {
        this.refreshTrigger++
        if (event.target && event.target !== this.activeView) {
          this.activeView = event.target
          router.push({ name: event.target })
        }
      }
    },

    navigate(view, filters = {}) {
      this.activeView = view
      this.filters = filters
      router.push({ name: view, query: filters })
    },
  },
})
