<script setup>
// App.vue now essentially just renders the current route
</script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
/* Global transitions handled in style.css or here */
</style>
