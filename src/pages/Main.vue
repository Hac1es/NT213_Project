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
              {{ config.targetApp || "Targert Application" }}
            </h2>
            <p class="text-white font-medium text-sm">
              <span>Auditor:</span>
              {{ config.auditorName || "Unknown" }}
            </p>
          </div>
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
            <span class="text-white font-bold">Level {{ config.level }}</span>
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
          secondary
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
          class="w-64 h-14 text-[#101014] font-black tracking-widest rounded-xl shadow-[0_0_30px_rgba(99,226,183,0.3)]"
          @click="calculateScore"
        >
          FINISH ASSESSMENT
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from "vue";
import { NButton, NProgress } from "naive-ui";
import ClickCriteria from "../components/ClickCriteria.vue";
import asvsData from "../assets/asvsData.json"; // Dữ liệu từ Python

const props = defineProps({
  config: { type: Object, required: true },
});

const currentStep = ref(0);
const results = reactive({});

// Lấy số Chapter từ ID (V1.1.1 -> 1)
const getChapterNumber = (chapter) => {
  if (!chapter.requirements.length) return "?";
  const firstId = chapter.requirements[0].id; // Ví dụ "V1.1.1"
  return firstId.split(".")[0].replace("V", "");
};

// Logic lọc Level theo mảng
const filteredData = computed(() => {
  const selectedLvl = Number(props.config.level);
  return asvsData
    .map((chapter) => {
      // Chỉ lấy req có mảng level chứa level đang chọn
      const matchedReqs = chapter.requirements.filter(
        (req) => Array.isArray(req.level) && req.level.includes(selectedLvl)
      );
      return { ...chapter, requirements: matchedReqs };
    })
    .filter((chapter) => chapter.requirements.length > 0);
});

const currentChapter = computed(() => filteredData.value[currentStep.value]);

function nextStep() {
  currentStep.value++;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function prevStep() {
  currentStep.value--;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function calculateScore() {
  [cite_start]; // Tính điểm định lượng (1=Pass, 0.5=Partial, 0=Fail) [cite: 1160, 1162, 1166]
  let totalPoints = 0;
  let applicableCount = 0;

  Object.values(results).forEach((val) => {
    if (typeof val === "number") {
      totalPoints += val;
      applicableCount++;
    }
  });

  const finalScore =
    applicableCount > 0 ? (totalPoints / applicableCount) * 10 : 0;

  [cite_start]; // Rating theo bảng quy đổi trong Paper [cite: 1242]
  let rating = "No Security";
  if (finalScore >= 9.0) rating = "Excellent Security";
  else if (finalScore >= 7.0) rating = "Good Security";
  else if (finalScore >= 4.0) rating = "Moderate Security";
  else if (finalScore >= 1.0) rating = "Low Security";

  alert(
    `Your Security Score: ${finalScore.toFixed(2)}/10\nAssessment: ${rating}`
  );
}
</script>
