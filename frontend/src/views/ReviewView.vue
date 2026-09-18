<template>
  <section v-if="result">
    <h2>저장 전 검토</h2>
    <p><span class="badge" :class="grade">{{ GRADE_LABEL[grade] }}</span>
      <span v-if="result.sources[0]" class="evidence"> · <a :href="result.sources[0].url" target="_blank">{{ result.sources[0].title || result.sources[0].url }}</a></span></p>

    <div class="card">
      <label>제목</label><input v-model="form.title" />
    </div>

    <table v-if="fields.length">
      <thead><tr><th>필드</th><th>SNS</th><th>공식</th><th>상태</th></tr></thead>
      <tbody>
        <tr v-for="f in fields" :key="f.field" :class="f.status">
          <td>{{ f.field }}</td>
          <td>{{ fmt(f.sns_value) }}</td>
          <td>{{ fmt(f.official_value) }}<div v-if="f.evidence" class="evidence">근거: {{ f.evidence }}</div></td>
          <td>{{ STATUS_LABEL[f.status] }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else class="evidence">공식 출처를 찾지 못했어요. SNS 값 기준으로 임시 저장할 수 있어요.</p>

    <div class="card">
      <label>신청 기간</label>
      <div style="display:flex; gap:8px;">
        <input type="date" v-model="form.fields.apply_period.start" @change="markOverride('apply_period')" />
        <input type="date" v-model="form.fields.apply_period.end" @change="markOverride('apply_period')" />
      </div>
      <p v-if="ambiguous" style="color:#d9822b; font-size:13px">날짜가 모호해요. 확인 후 저장할 수 있어요.</p>
    </div>

    <button :disabled="saving || ambiguous" @click="save">{{ fields.length ? '공식 정보 기준으로 저장' : 'SNS 값으로 임시 저장' }}</button>
    <p v-if="error" style="color:#d2323f">{{ error.message }}</p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getShareResult, createItem } from '../api/nexto'

const GRADE_LABEL = { HIGH: '공식 근거 있음', REVIEW: '확인 필요', UNVERIFIED: '공식 미확인' }
const STATUS_LABEL = { VERIFIED: '확인됨', REFINED: '공식 정보로 보완', CONFLICT: '차이 확인 필요', ADDED: '공식 정보에서 추가', AMBIGUOUS: '사용자 확인 필요', UNVERIFIED: '공식 미확인' }
const route = useRoute(), router = useRouter()
const result = ref(null), form = ref(null), saving = ref(false), error = ref(null), overrides = ref(new Set())

const fields = computed(() => result.value?.verification?.fields ?? [])
const grade = computed(() => result.value?.verification?.overall_grade ?? 'UNVERIFIED')
const ambiguous = computed(() => form.value?.fields.apply_period.status === 'ambiguous' && !overrides.value.has('apply_period'))
const fmt = v => Array.isArray(v) ? v.join(', ') : (v ?? '-')
const markOverride = f => { overrides.value.add(f); form.value.fields.apply_period.status = 'exact' }

// 추출값을 편집 폼으로 복사 (공식값 우선 적용은 TODO)
onMounted(async () => {
  result.value = await getShareResult(route.params.shareId)
  const ex = result.value.extraction
  form.value = { title: ex.title, category: ex.category, fields: { ...ex, apply_period: { ...ex.apply_period } } }
})

async function save() {
  saving.value = true; error.value = null
  try {
    const item = await createItem({ share_id: route.params.shareId, extraction_id: result.value.extraction.extraction_id, title: form.value.title,
      category: form.value.category, fields: form.value.fields, user_overrides: [...overrides.value], primary_source_id: result.value.sources[0]?.source_id ?? null })
    router.push(`/items/${item.item_id}`)
  } catch (e) { error.value = e } finally { saving.value = false }
}
</script>
