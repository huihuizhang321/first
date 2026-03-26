import http from './index'

export const taskApi = {
  list: (params) => http.get('/crm/tasks/', { params }),
  get: (id) => http.get(`/crm/tasks/${id}/`),
  create: (data) => http.post('/crm/tasks/', data),
  update: (id, data) => http.patch(`/crm/tasks/${id}/`, data),
  delete: (id) => http.delete(`/crm/tasks/${id}/`),
}
