<template>
  <header class="nav">
    <RouterLink to="/" class="brand">NEXTO</RouterLink>
    <nav>
      <RouterLink to="/">수집</RouterLink>
      <RouterLink to="/calendar">캘린더</RouterLink>
      <RouterLink to="/items">저장</RouterLink>
    </nav>
  </header>
  <main class="container"><RouterView /></main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
onMounted(() => useAuthStore().ensureSession())
</script>
