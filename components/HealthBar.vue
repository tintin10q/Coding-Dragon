<script setup lang="ts">


const {maxHealth = 100, health = 100} = defineProps<{maxHealth: number, health: number, name: string}>()
</script>

<template>
  <span style="padding-bottom: 2rem;  font-style: normal; font-size: 30pt "><b>{{name}}</b></span>
  <div style="display: flex; padding-bottom: 5rem">
    <div v-for="(_, index) in Array(maxHealth)"
         :style="{background: health > index ? 'green' : 'red', color: 'transparent', width: `${400/maxHealth}px`, height: '20px'}"
         :key="index"
    >
      ♥
    </div>
  </div>
</template>

<style scoped>

</style>