<template>
  <section v-if="item">
    <h2>{{ item.title }} <span class="badge" :class="item.overall_grade">{{ item.overall_grade }}</span></h2>
    <div class="card" v-if="item.source">
      <strong>공식 출처</strong><br>
      <a :href="item.source.url" target="_blank">{{ item.source.title || item.source.url }}</a>
      <div class="evidence">{{ item.source.domain_type }} · 검증 {{ item.last_verified_at?.slice(0, 16).replace('T', ' ') }}</div>
    </div>
    <div class="card"><strong>일정</strong>
      <div v-for="e in item.events" :key="e.event_type">{{ e.event_type }} · {{ e.start_at.slice(0, 10) }}</div>
    </div>
    <div class="card" v-if="item.fields.requirements?.length"><strong>준비 항목</strong>
      <ul><li v-for="r in item.fields.requirements" :key="r">{{ r }}</li></ul>
    </div>
    <table v-if="item.verification_fields.length">
      <thead><tr><th>필드</th><th>저장값</th><th>상태</th></tr></thead>
      <tbody>
        <tr v-for="f in item.verification_fields" :key="f.field" :class="f.status">
          <td>{{ f.field }}</td><td>{{ f.official_value ?? f.sns_value }}<div class="evidence" v-if="f.evidence">{{ f.evidence }}</div></td><td>{{ f.status }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getItem } from '../api/nexto'
const route = useRoute(), item = ref(null)
onMounted(async () => (item.value = await getItem(route.params.itemId)))
</script>
