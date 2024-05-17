<script setup lang="ts">

const {username} = defineProps<{ username: string }>()

const {data: scores} = useFetch(`/api/warrior`, {
  query: {username: username},
})

</script>

<template>
  <table>
    <thead>
    <tr>
      <th>Difficulty</th>
      <th>Score</th>
    </tr>
    </thead>
    <tbody>
    <tr>
      <td>Easy</td>
      <td>{{ scores?.easy }}</td>
    </tr>
    <tr>
      <td>Medium</td>
      <td>{{ scores?.medium }}</td>
    </tr>
    <tr>
      <td>Hard</td>
      <td>{{ scores?.hard }}</td>
    </tr>
    </tbody>
  </table>
</template>

<style scoped>
table {
  width: 80%;
  margin: 20px auto;
  border-collapse: collapse;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
  font-size: larger;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: rgba(83, 242, 147, 0.53);
}

tr:hover {
  background-color: #ddd;
}
</style>