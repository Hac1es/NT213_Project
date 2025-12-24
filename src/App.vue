<script setup>
import { NConfigProvider, NMessageProvider } from "naive-ui";
</script>

<template>
  <NConfigProvider>
    <NMessageProvider>
      <router-view />
    </NMessageProvider>
  </NConfigProvider>
</template>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: auto;
}
</style>
