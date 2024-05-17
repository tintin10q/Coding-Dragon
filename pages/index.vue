<script setup lang="ts">

</script>

<template>
  <div style="display: flex; justify-content: center; font-size: x-large; height: 99dvh; align-items: center">
    <div style="margin-inline: 10dvw; margin-top: 1dvh">
      <p>Hi there! Do you want to fight the dragon?</p>
      <img src="/draak.png" style="width: 20rem; opacity: .70" class="shimmer">
      <button>
        <router-link to="/signup">Sign up here!</router-link>
      </button>
    </div>
  </div>
</template>

<style scoped>
.shimmer {
  color: grey;
  display:inline-block;
  -webkit-mask:linear-gradient(-60deg,#000 30%,#0005,#000 70%) right/300% 100%;
  background-repeat: no-repeat;
  animation: shimmer 2.5s infinite;
  font-size: 50px;
  max-width:200px;
}

@keyframes shimmer {
  100% {-webkit-mask-position:left}
}
</style>