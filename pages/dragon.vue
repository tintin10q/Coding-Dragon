<script setup lang="ts">
import HealthBar from "~/components/HealthBar.vue";

const WS_URL = 'ws://localhost:8001/'

const max_health = ref(5000)

const damage_death = ref(new Map())
if (process.client) {
  damage_death.value = load_damage()
  max_health.value += 1;
  // hack to make health bar update
  setTimeout(() => {
    max_health.value -= 1;
    if (websocket && calc_health() < 0) {
      websocket.close()
    }
  }, 2)
}

const easy_damage = 1
const medium_damage = easy_damage * 3
const hard_damage = medium_damage * 2

function deal_damage(username: string, amount: number) {
  const my_damage = damage_death.value.get(username) ?? 0
  damage_death.value.set(username, my_damage + amount)
  last_damage_done.value = amount
  if (allowed_audio.value) {
    if (amount >= hard_damage) hit_sound_hard.play()
    else if (amount >= medium_damage) hit_sound_medium.play()
    else if (amount >= easy_damage) hit_sound_easy.play()
  }
}

const last_damage_done = ref(0)

watch(last_damage_done, () => {
  setTimeout(() => (last_damage_done.value = 0), 3000)
})

const sorted_damage_dealt = computed(() => {
  const entries = damage_death.value.entries()
  return Array(...entries).sort((a, b) => b[1] - a[1])
})

function calc_health() {
  let h = max_health.value;
  for (const damage of damage_death.value.values()) h -= damage;
  return h;
}

const health = computed(calc_health)

function showMessage(msg) {
  console.log(msg)
  message.value = msg;
}

let websocket: WebSocket;

let hit_sound_easy: Audio
let hit_sound_medium: Audio
let hit_sound_hard: Audio


const allowed_audio = ref(false);
let died = ref(false);

if (process.client) {

  hit_sound_easy = new Audio('/hit.mp3')
  hit_sound_medium = new Audio('/medium_damage.ogx')
  hit_sound_hard = new Audio('/big_damage.ogx')

  onMounted(() => {
    websocket = new WebSocket(WS_URL);
    websocket.addEventListener("message", handle_msg)
  })

  onUnmounted(() => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.close()
    }
  })


  function handle_msg({data}) {
    const event = JSON.parse(data);
    console.log("event", event)
    if (died.value) return;
    let username, damage;
    switch (event.type) {
      case "damage":
        username = event.data.username;
        damage = event.data.damage;
        showMessage(`${username} deals ${damage} damage!`);
        deal_damage(username, damage)
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  }
}

const message = ref("")


function save_damage(damages: Map<string, number>) {
  const to_save = [...damages.entries()];
  localStorage.setItem("damages", JSON.stringify(to_save));
}

function load_damage(): Map<string, number> {
  return new Map(JSON.parse(localStorage.getItem("damages") ?? null) ?? []);
}

watch(health, (new_health) => {
  console.log("New health", new_health)
  if (0 >= new_health && !died.value) {
    died.value = true;
    showMessage("The Dragon has been beaten!")
    websocket.close();
    if (allowed_audio.value) {
      const victory_sound = new Audio('/victory.ogx')
      console.log("audio",victory_sound)
      victory_sound.play()
    }
  }
  save_damage(damage_death.value)
})

function reset() {
  damage_death.value = new Map();
  message.value = ''
  window.location.reload()
}

</script>

<template>
  <div style="position: absolute; left: 40%; top: 50%; transform: translate(-50%, -50%); z-index: 2"
       v-show="last_damage_done > 0">
    <img src="/damage.png" style="height: 3rem; position: absolute">
    <span style="font-size: x-large; position: absolute; left: .8rem; top: 13px">{{ last_damage_done }}</span>
  </div>
  <div
      style="padding: 4rem; color: #E01E79; font-size: xx-large; position: absolute; display: flex; align-items: center; gap: 1rem">
    <button v-if="damage_death.size > 0" @click="reset()">❌</button>
    <button @click="allowed_audio = !allowed_audio">{{ allowed_audio ? '🔊' : '🔇' }}</button>
    {{ message }}
  </div>
  <div style="padding: 4rem"></div>

  <div style="display: flex; margin-inline: 5rem">
    <div
        style="display: flex; align-content: center; align-items: center; justify-content: center;
        padding-right: 8rem;
        padding-left: 20rem;
        flex-direction: column">
      <health-bar :class="{'disappear-animation': !died}" v-if="!died" :health="health" :max-health="max_health"
                  name="The Dragon"/>
      <div>
        <img src="/draak.png" :style="{'max-height': '30rem'}"
             :class="{'death-animation': 0 >= health , 'dragon-move': !died}">
      </div>
    </div>
    <div style="position: relative" v-if="damage_death.size">
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


@keyframes death {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5) rotateZ(90deg);
  }
  100% {
    transform: scale(0) rotateZ(180deg);
    opacity: 0;
  }
}

@keyframes disappear {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 0;
  }
}

.disappear-animation {
  animation: disappear 2s forwards;
}

.death-animation {
  animation: death 4s forwards;
}

@keyframes dragonMove {
  0% {
    transform: translateX(-1%);
  }
  50% {
    transform: translateX(1%);
  }
  100% {
    transform: translateX(-1%);
  }
}

.dragon-move {
  animation: dragonMove 2s ease-in-out infinite;
}

</style>

