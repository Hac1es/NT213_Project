<template>
  <div class="w-full bg-[#101014] text-white py-10 min-h-screen">
    <div class="w-[80%] mx-auto flex flex-col pb-32">
      <div
        class="mb-8 p-6 border border-[#63e2b7]/30 rounded-lg bg-[#18181c]/95 sticky top-5 z-50 shadow-2xl backdrop-blur-md"
      >
        <div class="flex justify-between items-center mb-4">
          <div>
            <h2
              class="text-[#63e2b7] font-bold text-xl uppercase tracking-wider"
            >
              {{ store.config.targetApp || "Targert Application" }}
            </h2>
            <p class="text-white font-medium text-sm">
              <span>Auditor:</span>
              {{ store.config.auditorName || "Unknown" }}
            </p>
          </div>

          <n-button
            @click="devQuickFill"
            size="small"
            ghost
            type="warning"
            class="opacity-50 hover:opacity-100"
          >
            [DEV] Random Fill & Finish
          </n-button>

          <div class="text-right">
            <span
              class="text-xs uppercase text-shadow-white font-bold tracking-widest"
              >Progress</span
            >
            <div class="text-[#63e2b7] font-black text-2xl leading-none">
              {{ currentStep + 1 }}
              <span class="text-gray-600 text-lg"
                >/ {{ filteredData.length }}</span
              >
            </div>
          </div>
        </div>
        <n-progress
          type="line"
          :percentage="((currentStep + 1) / filteredData.length) * 100"
          :show-indicator="false"
          color="#63e2b7"
          rail-color="rgba(99,226,183,0.1)"
        />
      </div>

      <div v-if="currentChapter">
        <div class="mb-10">
          <h1
            class="text-3xl font-bold text-gray-100 flex items-baseline gap-4"
          >
            <span class="text-[#63e2b7] shrink-0 font-mono text-4xl"
              >V{{ getChapterNumber(currentChapter) }}</span
            >
            <span
              class="border-l border-gray-800 pl-5 capitalize font-semibold tracking-tight"
            >
              {{ currentChapter.chapterName }}
            </span>
          </h1>
          <p class="text-gray-500 italic mt-4 ml-20 text-lg">
            This chapter contains
            <span class="text-[#63e2b7] font-bold">{{
              currentChapter.requirements.length
            }}</span>
            requirements for
            <span class="text-white font-bold"
              >Level {{ store.config.level }}</span
            >
            of ASVS framework.
          </p>
        </div>

        <div class="space-y-8 bg-[#18181c]/30 pt-2 pb-8 rounded-3xl">
          <ClickCriteria
            v-for="req in currentChapter.requirements"
            :key="req.id"
            :heading="req.id + '.'"
            :title="req.text"
            :ref-label="req.refLabel"
            :ref-url="req.refUrl"
            v-model="results[req.id]"
          />
        </div>
      </div>

      <div class="mt-16 flex justify-between items-center">
        <n-button
          size="large"
          ghost
          color="#63e2b7"
          class="w-48 h-14 font-bold rounded-xl"
          :disabled="currentStep === 0"
          @click="prevStep"
        >
          <span
            :class="
              currentStep === 0
                ? 'text-lg'
                : 'hover:underline underline-offset-4 text-lg'
            "
          >
            ← BACK
          </span>
        </n-button>

        <n-button
          v-if="currentStep < filteredData.length - 1"
          size="large"
          color="#63e2b7"
          class="w-56 h-14"
          @click="nextStep"
        >
          <span class="text-[#101014] text-lg font-semibold">NEXT CHAPTER</span>
        </n-button>

        <n-button
          v-else
          size="large"
          color="#63e2b7"
          class="w-64 h-14 shadow-[0_0_30px_rgba(99,226,183,0.3)]"
          @click="calculateScore"
        >
          <span class="text-[#101014] rounded-xl font-semibold"
            >FINISH ASSESSMENT</span
          >
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from "vue";
import { useRouter } from "vue-router";
import { NButton, NProgress, useMessage } from "naive-ui";
import ClickCriteria from "../components/ClickCriteria.vue";

// Import dữ liệu và Store
import asvsData from "../assets/asvsData.json";
import { useAssessmentStore } from "../stores/assessmentStore";

const store = useAssessmentStore();
const router = useRouter();
const message = useMessage();

// --- LOGIC GIAO DIỆN (CẦN PHẢI CÓ ĐỂ TEMPLATE KHÔNG LỖI) ---
const currentStep = ref(0);
const results = reactive({});
const isLoading = ref(false);

// Lấy số Chapter từ ID (V1.1.1 -> 1)
const getChapterNumber = (chapter) => {
  if (!chapter.requirements.length) return "?";
  const firstId = chapter.requirements[0].id;
  return firstId.split(".")[0].replace("V", "");
};

// Logic lọc Level theo mảng
const filteredData = computed(() => {
  const selectedLvl = Number(store.config.level);
  return asvsData
    .map((chapter) => {
      const matchedReqs = chapter.requirements.filter(
        (req) => Array.isArray(req.level) && req.level.includes(selectedLvl)
      );
      return { ...chapter, requirements: matchedReqs };
    })
    .filter((chapter) => chapter.requirements.length > 0);
});

// Chapter đang hiển thị
const currentChapter = computed(() => filteredData.value[currentStep.value]);

function nextStep() {
  currentStep.value++;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function prevStep() {
  currentStep.value--;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// --- LOGIC TÍNH TOÁN & CHUYỂN TRANG (Đổi tên thành calculateScore cho khớp Template) ---
async function calculateScore() {
  isLoading.value = true;

  try {
    // 1. Lưu điểm checklist hiện tại vào Store
    store.saveResults(results);

    // 2. Chạy hàm tính 5 tầng trong Store
    const report = await store.generateReport();

    if (report) {
      message.success("Calculation complete!");
      // Chuyển sang Result, không cần query vì Result sẽ lấy data từ Store
      router.push({ name: "Result" });
    }
  } catch (error) {
    console.error(error);
    message.error("Calculation failed. Please check your inputs.");
  } finally {
    isLoading.value = false;
  }
}

function devQuickFill() {
  // 1. Duyệt qua toàn bộ JSON để lấy hết ID
  asvsData.forEach((chapter) => {
    chapter.requirements.forEach((req) => {
      // 2. Random điểm 0, 0.5, 1 cho mỗi câu
      results[req.id] = [0, 0.5, 1][Math.floor(Math.random() * 3)];
    });
  });

  // 3. Gọi luôn hàm Finish để tính toán và chuyển trang
  calculateScore();
}
</script>
