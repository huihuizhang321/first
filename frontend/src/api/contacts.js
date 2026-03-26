import http from './index'

export const contactApi = {
  list: (params) => http.get('/crm/contacts/', { params }),
  get: (id) => http.get(`/crm/contacts/${id}/`),
  create: (data) => http.post('/crm/contacts/', data),
  update: (id, data) => http.patch(`/crm/contacts/${id}/`, data),
  delete: (id) => http.delete(`/crm/contacts/${id}/`),
}
