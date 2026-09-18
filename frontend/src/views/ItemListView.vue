<template>
  <section>
    <h2>저장한 정보</h2>
    <div v-for="i in items" :key="i.item_id" class="card">
      <RouterLink :to="`/items/${i.item_id}`"><strong>{{ i.title }}</strong></RouterLink>
      <span class="badge" :class="i.overall_grade" style="margin-left:8px">{{ i.overall_grade }}</span>
      <div class="evidence">{{ i.category }} · {{ i.status }}</div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getItems } from '../api/nexto'
const items = ref([])
onMounted(async () => (items.value = await getItems()))
</script>
