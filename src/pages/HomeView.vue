<template>
  <div
    ref="containerRef"
    class="h-screen w-full overflow-y-auto scroll-smooth snap-y snap-mandatory bg-[#101014]"
  >
    <section class="h-screen w-full snap-start shrink-0 relative z-20">
      <LandingPage @start="scrollToMain" />
    </section>

    <section
      id="main-content"
      class="min-h-screen w-full snap-start relative z-10"
    >
      <MainPage />
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import LandingPage from "./LandingPage.vue"; // Đường dẫn tới file Landing của bạn
import MainPage from "./Main.vue"; // Đường dẫn tới file Main của bạn

const containerRef = ref(null);

// Hàm cuộn xuống Main Page
function scrollToMain() {
  const mainSection = document.getElementById("main-content");
  if (mainSection && containerRef.value) {
    // Cách 1: Dùng native scroll (mượt nhờ class scroll-smooth ở div cha)
    mainSection.scrollIntoView({ behavior: "smooth" });
  }
}
</script>
