import http from './index'

export const dealApi = {
  list: (params) => http.get('/crm/deals/', { params }),
  get: (id) => http.get(`/crm/deals/${id}/`),
  create: (data) => http.post('/crm/deals/', data),
  update: (id, data) => http.patch(`/crm/deals/${id}/`, data),
  delete: (id) => http.delete(`/crm/deals/${id}/`),
}
