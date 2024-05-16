<script setup lang="ts">


import {useLocalStorage} from "@vueuse/core";
import {ref, reactive} from "vue";
import z from "zod";


const username = useLocalStorage("leetcodeusername")

const errorMSG = ref("")

let loading = ref(false);

const parseError = z.object({"data": z.object({"message": z.string()})})

async function signup() {
  if (loading.value) return;
  errorMSG.value = "";
  if (!given_username.value) return;
  loading.value = true;
  try {
    const profile = await $fetch("/api/warrior?username=" + given_username.value, {
      method: "POST"
    })
    username.value = given_username.value;
    given_username.value = ""
  } catch (error) {
    const parsedError = parseError.safeParse(error);
    if (parsedError.success) errorMSG.value = parsedError.data.data.message;
    else {
      errorMSG.value = error;
    }
    return;
  } finally {
    loading.value = false;
  }
}

function signout() {
  $fetch("/api/warrior?username=" + username.value, {
    method: "DELETE"
  })
  username.value = null;
}

const given_username = ref("")

// Get all usernames with GET


</script>

<template>
  <div v-if="!username" style="display: flex; justify-content: center">
    <div>
      <h1>Sign up to slay dragon</h1>
      <p>Hoi dit is een signup page 🐉🗡️</p>
      <form>
        <label style="font-size: large" for="username">Username:</label>
        <input style="font-size: large" name="username" type="text" v-model="given_username">
        <button type="submit" @click.prevent="signup()">Signup</button>
      </form>
    </div>
  </div>
  <div v-else>
    <div style="display: flex;justify-content: center">
    <span style="font-size: larger">
    You signed up as <b>{{ username }}</b>
      </span>
    </div>
    <scores :username="username" style="max-width: 10rem"></scores>
    <div style="display: flex; justify-content: center">
      <button type="button" @click="signout()">Remove my username</button>
    </div>
  </div>
  <div style="display: flex; justify-content: center">
    <div v-show="errorMSG.length !== 0"
         style="color: darkred; padding: 1rem; border: black solid 2px; width: fit-content">
      Error: {{ errorMSG }}
    </div>
    <loader v-show="loading === true"/>
  </div>
</template>

<style scoped>

</style>