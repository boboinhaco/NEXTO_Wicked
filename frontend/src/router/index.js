import { createRouter, createWebHistory } from 'vue-router'

// SCR-01~05 P0 + P1 홈/지도 자리
const routes = [
  { path: '/', component: () => import('../views/UploadView.vue') },
  { path: '/analyze/:jobId', component: () => import('../views/AnalyzeView.vue') },
  { path: '/review/:shareId', component: () => import('../views/ReviewView.vue') },
  { path: '/calendar', component: () => import('../views/CalendarView.vue') },
  { path: '/items', component: () => import('../views/ItemListView.vue') },
  { path: '/items/:itemId', component: () => import('../views/ItemDetailView.vue') }
]

export default createRouter({ history: createWebHistory(), routes })
