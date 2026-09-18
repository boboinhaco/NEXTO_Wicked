<template>
  <section>
    <h2>캘린더</h2>
    <div style="display:flex; gap:8px; align-items:center; margin-bottom:12px;">
      <button class="ghost" @click="shift(-1)">‹</button><strong>{{ ym }}</strong><button class="ghost" @click="shift(1)">›</button>
    </div>
    <!-- TODO: 월 그리드 UI, 지금은 목록 -->
    <div v-for="e in events" :key="e.event_id" class="card">
      <span class="evidence">{{ e.start_at.slice(0, 10) }}</span> · {{ TYPE[e.event_type] ?? e.event_type }} ·
      <RouterLink :to="`/items/${e.item_id}`">{{ e.title }}</RouterLink>
      <span v-if="e.date_status === 'AMBIGUOUS'" class="evidence"> (날짜 확인 필요)</span>
    </div>
    <p v-if="!events.length" class="evidence">이 달에는 일정이 없어요.</p>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { getCalendar } from '../api/nexto'

const TYPE = { APPLY_START: '신청 시작', APPLY_END: '신청 마감', EVENT_PERIOD: '행사', VISIT: '방문' }
const cursor = ref(new Date()), events = ref([])
const ym = computed(() => `${cursor.value.getFullYear()}-${String(cursor.value.getMonth() + 1).padStart(2, '0')}`)
const shift = n => { cursor.value = new Date(cursor.value.getFullYear(), cursor.value.getMonth() + n, 1) }

// 월 범위 조회
async function load() {
  const y = cursor.value.getFullYear(), m = cursor.value.getMonth()
  const last = new Date(y, m + 1, 0).getDate()
  events.value = await getCalendar(`${ym.value}-01`, `${ym.value}-${last}`)
}
watch(ym, load, { immediate: true })
</script>
