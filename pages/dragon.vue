<script setup lang="ts">
import HealthBar from "~/components/HealthBar.vue";

const max_health = ref(500)

const damage_death = ref(new Map<string, number>())

damage_death.value.set("tintin10q", 20)
/*
damage_death.value.set("Quint", 13)
damage_death.value.set("Quint2", 12)
damage_death.value.set("Quint3", 12)
damage_death.value.set("Quint4", 12)
damage_death.value.set("Quint5", 12)
damage_death.value.set("Quint6", 12)
damage_death.value.set("Quint8", 19)
damage_death.value.set("Quint9", 12)

 */

const sorted_damage_dealt = computed(() => {
  return Array(...damage_death.value.entries()).sort((a, b) => b[1] - a[1])
})

const health = computed(() => {
  let h = max_health.value;
  for (const damage of damage_death.value.values()) h -= damage;
  return h;
})

</script>

<template>
  <div style="padding: 4rem">
  </div>

  <div style="display: flex; margin-inline: 5rem">
    <div
        style="display: flex; align-content: center; align-items: center; justify-content: center;
        padding-right: 8rem;
        padding-left: 20rem;
        flex-direction: column">
      <health-bar :health="health" :max-health="max_health" name="The Dragon"/>
      <div>
        <img src="/draak.png" style="max-height: 30rem;">
      </div>
    </div>
    <div style="position: relative"  v-if="damage_death.size">
      <img src="/human.png" style="width: auto; height: 40rem; display: block">
      <div class="item-list">
        <div class="item" v-for="([name, damage], index) in sorted_damage_dealt" :key="name + damage">
          <div style="display: flex; align-items: center">
            <img :src="index === 0 ? '/king.png' : '/peasent.png' " style="height: 5rem">
            <div>
              <span style="font-size: larger; padding-left: .25rem">{{ name }}</span>
              <br>
              <span style="font-size: large; padding-left: .25rem">{{ Math.round(damage / max_health * 100) }}% of damage dealt</span>
            </div>
          </div>
        </div>
        <!-- Add more items as needed -->
      </div>
    </div>
  </div>
</template>

<style scoped>

.item-list {
  position: absolute;
  top: 5rem;
  margin-inline: 3rem;
  left: 0;
  width: 85%;
  box-sizing: border-box;
  max-height: 488px;
  overflow-y: scroll;
  overflow-x: hidden;
}

.item-list::-webkit-scrollbar {
  width: 12px;
}

.item-list::-webkit-scrollbar-track {
  background: transparent;
}

.item-list::-webkit-scrollbar-thumb {
  background: rgba(103, 77, 77, 0.8);
}

.item-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.item-list::-webkit-scrollbar-button {
  display: none;
}

.item {
  padding: 5px 10px;
  margin-bottom: 5px; /* Add some space between items */
}

@font-face {
  font-family: Runescape;
  src: url(/runescape_bold.ttf);
}

</style>

<style>
body {
  background-image: url("/background.png");
  background-size: cover;
  color: white;
  font-family: Runescape, Arial, Helvetica, sans-serif;
}
</style>