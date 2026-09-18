import client from './client'

// 명세서 9장 API 래퍼
export const demoLogin = () => client.post('/auth/demo')
export const createShare = (formData) => client.post('/shares', formData)
export const getJob = (jobId) => client.get(`/jobs/${jobId}`)
export const retryJob = (jobId) => client.post(`/jobs/${jobId}/retry`)
export const getShareResult = (shareId) => client.get(`/shares/${shareId}/result`)
export const createItem = (body) => client.post('/items', body)
export const getItems = (params) => client.get('/items', { params })
export const getItem = (itemId) => client.get(`/items/${itemId}`)
export const patchItem = (itemId, body) => client.patch(`/items/${itemId}`, body)
export const getCalendar = (from, to) => client.get('/calendar', { params: { from, to } })

// SSE 구독, 실패 시 2초 polling으로 fallback
export const watchJob = (jobId, handlers) => {
  let timer = null
  const es = new EventSource(`/api/jobs/${jobId}/stream`)
  const stop = () => { es.close(); clearInterval(timer) }
  Object.entries(handlers).forEach(([ev, fn]) => es.addEventListener(ev, e => { fn(JSON.parse(e.data)); if (ev !== 'progress') stop() }))
  es.onerror = () => {
    es.close()
    timer = setInterval(async () => {
      const job = await getJob(jobId)
      if (job.status === 'COMPLETED') { handlers.completed?.(job); stop() }
      else if (job.status === 'FAILED') { handlers.failed?.(job.error); stop() }
      else handlers.progress?.(job)
    }, 2000)
  }
  return stop
}
