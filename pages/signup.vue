<script setup lang="ts">


import {useLocalStorage} from "@vueuse/core";

const username = useLocalStorage("leetcodeusername")

function signup() {
  $fetch("/api/warrior?username=" + given_username.value, {
    method:"POST"
  })
  username.value = given_username.value;
  given_username.value = ""
}

function signout() {
  $fetch("/api/warrior?username=" + username.value, {
    method:"DELETE"
  })
  username.value = null;
}

const given_username = ref("")

// Get all usernames with GET


</script>

<template>
  <div v-if="!username">
    <h1>Sign up to slay dragon</h1>
    <p>Hoi dit is een signup page</p>
    <form>
      <label for="username">Username:</label>
      <input name="username" type="text" v-model="given_username">
      <button type="button" @click="signup()">Signup</button>
    </form>
  </div>
  <div v-else>
    You signed up as "{{username}}"
    <button type="button" @click="signout()">Remove my username</button>
  </div>
</template>

<style scoped>

</style>