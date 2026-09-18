import axios from 'axios'

// envelope { success, data, error } 처리, JWT 자동 첨부
const client = axios.create({ baseURL: '/api' })
client.interceptors.request.use(cfg => {
  const token = localStorage.getItem('nexto_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})
client.interceptors.response.use(res => res.data.data, err => Promise.reject(err.response?.data?.error ?? { code: 'NETWORK', message: '서버에 연결할 수 없어요.', retryable: true }))

export default client
