<template>
  <div
    ref="containerRef"
    class="h-screen w-full overflow-y-auto scroll-smooth snap-y snap-mandatory bg-[#101014]"
  >
    <section id="hero" class="h-screen w-full snap-start shrink-0">
      <LandingPage @start="scrollToNext('about')" />
    </section>

    <section id="about" class="h-screen w-full snap-start shrink-0">
      <AboutSection @next="scrollToNext('guide')" />
    </section>

    <section id="guide" class="h-screen w-full snap-start shrink-0">
      <GuideSection />
    </section>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"; // Thêm reactive
import LandingPage from "./LandingPage.vue";
import MainPage from "./Main.vue";
import AboutSection from "./AboutSection.vue";
import GuideSection from "./GuideSection.vue";
import Input from "./Input.vue";

const containerRef = ref(null);

// 3. Khai báo trạng thái đánh giá tập trung
const assessmentState = reactive({
  targetApp: "",
  auditorName: "",
  level: 1, // Mặc định Level 1 theo ASVS
  isStarted: false,
});

function scrollToNext(id) {
  const nextSection = document.getElementById(id);
  if (nextSection) {
    nextSection.scrollIntoView({ behavior: "smooth" });
  }
}

// 4. Hàm xử lý khi người dùng hoàn tất nhập liệu ở trang Input
function handleInputComplete(data) {
  // Cập nhật dữ liệu từ Input vào state chung
  assessmentState.targetApp = data.targetApp;
  assessmentState.auditorName = data.auditorName;
  assessmentState.level = data.level;
  assessmentState.isStarted = true;

  // Tự động cuộn xuống phần đánh giá chính (MainPage)
  scrollToNext("main-content");
}
</script>
