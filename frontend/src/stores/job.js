import { defineStore } from 'pinia'
import { watchJob, retryJob } from '../api/nexto'

// 분석 Job 진행 상태
export const useJobStore = defineStore('job', {
  state: () => ({ jobId: null, stage: null, status: 'IDLE', message: '', result: null, error: null, stop: null }),
  actions: {
    subscribe(jobId) {
      this.stop?.(); this.$reset(); this.jobId = jobId; this.status = 'RUNNING'
      this.stop = watchJob(jobId, {
        progress: d => { this.stage = d.stage; this.message = d.message ?? '' },
        completed: d => { this.status = 'COMPLETED'; this.result = d },
        failed: d => { this.status = 'FAILED'; this.error = d }
      })
    },
    async retry() { await retryJob(this.jobId); this.subscribe(this.jobId) }
  }
})
