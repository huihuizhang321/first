import http from './index'

export const customerApi = {
  list: (params) => http.get('/crm/customers/', { params }),
  get: (id) => http.get(`/crm/customers/${id}/`),
  create: (data) => http.post('/crm/customers/', data),
  update: (id, data) => http.patch(`/crm/customers/${id}/`, data),
  delete: (id) => http.delete(`/crm/customers/${id}/`),
}
