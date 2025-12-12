<script setup>
import { ref, onMounted } from "vue";
import { NButton, NIcon } from "naive-ui";
import { ArrowForward, LockClosed, ShieldCheckmark } from "@vicons/ionicons5";
import { useRouter } from "vue-router";

// Định nghĩa emit để báo cho cha biết user muốn xuống dưới
const emit = defineEmits(["start"]);

const scrollIndicator = ref("Get Started!");
const isVisible = ref(false);

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});

function handleNavigate() {
  // Thay vì router.push, ta emit sự kiện
  emit("start");
}

// Xử lý sự kiện lăn chuột ở Landing Page
function handleWheel(e) {
  // Nếu lăn chuột xuống, kích hoạt chuyển trang
  if (e.deltaY > 20) {
    handleNavigate();
  }
}
</script>

<template>
  <div
    @wheel.passive="handleWheel"
    class="landing-page min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white overflow-hidden"
  >
    <!-- Hero Section -->
    <main class="relative min-h-screen flex items-center justify-center px-8">
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div
          class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-radial from-emerald-500/20 via-transparent to-transparent rounded-full blur-3xl animate-pulse-slow"
        ></div>

        <!-- Animated Lines -->
        <svg class="absolute inset-0 w-full h-full opacity-20">
          <line
            x1="10%"
            y1="20%"
            x2="50%"
            y2="50%"
            stroke="white"
            stroke-width="1"
            class="animate-draw"
          />
          <line
            x1="90%"
            y1="25%"
            x2="50%"
            y2="50%"
            stroke="white"
            stroke-width="1"
            class="animate-draw"
          />
          <line
            x1="10%"
            y1="80%"
            x2="50%"
            y2="50%"
            stroke="white"
            stroke-width="1"
            class="animate-draw"
          />
          <line
            x1="88%"
            y1="75%"
            x2="50%"
            y2="50%"
            stroke="white"
            stroke-width="1"
            class="animate-draw"
          />
        </svg>
      </div>

      <!-- Central Content -->
      <div
        class="relative z-10 flex items-center flex-col text-center max-w-4xl mx-auto"
        :class="{ 'animate-fade-in': isVisible, 'animate-fade-out': isExiting }"
      >
        <!-- Unlock Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-2">
          <span class="text-6xl text-white font-bold font-family-modern-antiqua"
            >Q-ASVS</span
          >
        </div>

        <h1
          class="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight"
        >
          Quantify Your Web Security
        </h1>

        <p class="text-lg md:text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
          Transform OWASP ASVS checklists into calculated security scores and
          actionable insights for strengths and weaknesses analysis.
        </p>

        <!-- Scroll Indicator -->
        <div
          class="flex items-center gap-5 text-sm text-gray-400 cursor-pointer"
          @click="handleNavigate"
          role="button"
          tabindex="0"
        >
          <div
            class="w-12 h-12 rounded-full border text-2xl border-white/20 flex items-center justify-center animate-bounce"
          >
            ↓
          </div>
          <span class="text-2xl font-bold">{{ scrollIndicator }}</span>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse-slow {
  0%,
  100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-out {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}

@keyframes draw {
  from {
    stroke-dashoffset: 1000;
  }
  to {
    stroke-dashoffset: 0;
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}

.animate-fade-out {
  animation: fade-out 0.6s ease-in forwards;
}

.animate-draw {
  stroke-dasharray: 1000;
  animation: draw 3s ease-in-out infinite;
}

.bg-gradient-radial {
  background: radial-gradient(circle, var(--tw-gradient-stops));
}
</style>
