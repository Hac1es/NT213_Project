<script setup>
import { NConfigProvider } from "naive-ui";
</script>

<template>
  <NConfigProvider>
    <router-view />
  </NConfigProvider>
</template>

<style>
/* Đảm bảo html và body chiếm hết màn hình để tính năng scroll hoạt động tốt */
html,
body,
#app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: auto;
}
</style>
