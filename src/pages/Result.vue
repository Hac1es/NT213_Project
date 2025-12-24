<template>
  <div class="min-h-screen bg-[#101014] text-white py-12">
    <div class="w-[80%] mx-auto">
      <div
        class="flex justify-between items-end mb-12 border-b border-gray-800 pb-8"
      >
        <div>
          <h1 class="text-[#63e2b7] text-3xl font-black mb-2">FINAL REPORT</h1>
          <p class="text-gray-400 italic">
            Quantitative assessment for
            <span class="text-white font-bold">{{ config.targetApp }}</span>
          </p>
        </div>
        <div class="text-right text-white font-mono">
          <p>Auditor: {{ config.auditorName }}</p>
          <p>ASVS Level: {{ config.level }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-5">
        <div
          class="p-8 rounded-3xl border border-[#63e2b7]/20 flex flex-col items-center justify-center relative overflow-hidden shadow-2xl"
        >
          <div
            class="absolute top-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-[#63e2b7] to-transparent"
          ></div>

          <span
            class="text-gray-500 uppercase tracking-[0.3em] font-bold text-lg mb-6"
            >Score of SOI</span
          >

          <n-progress
            type="circle"
            :percentage="score * 10"
            :stroke-width="6"
            color="#63e2b7"
            rail-color="rgba(99,226,183,0.05)"
            class="w-48"
          >
            <div class="text-center">
              <div class="text-4xl font-black text-white">{{ score }}</div>
              <div class="text-gray-500 font-bold">/ 10</div>
            </div>
          </n-progress>

          <div
            :class="[
              'mt-8 px-6 py-2 rounded-full font-black text-sm uppercase tracking-widest border',
              ratingColor,
            ]"
          >
            {{ rating }}
          </div>
        </div>

        <div
          class="lg:col-span-2 p-8 rounded-3xl border border-white/5 flex flex-col shadow-inner"
        >
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr
                  class="text-gray-500 uppercase text-[10px] tracking-[0.2em] border-b border-gray-800/50"
                >
                  <th class="pb-4 font-black">Evaluation Aspect</th>
                  <th class="pb-4 font-black text-center">Avg Score (S)</th>
                  <th class="pb-4 font-black text-center">Weight (W)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-800/30">
                <tr
                  v-for="item in chapterScores"
                  :key="item.aspect"
                  class="group transition-colors hover:bg-white/5"
                >
                  <td class="py-6">
                    <div class="flex flex-col gap-2">
                      <span
                        class="text-gray-200 font-bold tracking-tight text-base"
                        >{{ item.aspect }}</span
                      >
                      <n-progress
                        type="line"
                        :percentage="item.score * 100"
                        :show-indicator="false"
                        :height="4"
                        color="#63e2b7"
                        rail-color="rgba(99,226,183,0.05)"
                        class="w-32"
                      />
                    </div>
                  </td>
                  <td class="py-6 text-center">
                    <span class="font-mono text-[#63e2b7] text-lg font-medium">
                      {{ item.score.toFixed(3) }}
                    </span>
                  </td>
                  <td class="py-6 text-center">
                    <span class="text-gray-400 font-mono">
                      {{ (item.weight * 100).toFixed(0) }}%
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <p class="mt-6 text-gray-500 text-xs italic leading-relaxed">
            * Note: The SOI Score is calculated as the sum of (S × W) across the
            three assessment aspects, multiplied by a factor of 10 to yield a
            standardized score.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-20">
        <n-button
          block
          ghost
          text-color="#63E2B7"
          size="large"
          class="h-12 font-semibold border border-[#2E3235] hover:(bg-[#1F2224] text-[#6AF5B3]) shadow-[inset_0_0_12px_#0D1512,0_0_6px_#0D1512] transition-all duration-300"
          @click="retake"
        >
          RE-ASSESS SYSTEM
        </n-button>

        <n-button
          block
          color="#4ADEA3"
          text-color="#0F1114"
          size="large"
          class="h-14 font-black tracking-widest shadow-lg shadow-emerald-400/20 hover:(bg-[#3DD497]) transition-all duration-300"
          @click="openDetails"
        >
          GET DETAILS
        </n-button>
      </div>

      <div
        class="min-h-screen bg-[#101014] text-white mt-24"
        v-show="showDrawer"
        ref="detailsSection"
      >
        <div class="mx-auto">
          <n-tabs type="card" animated class="custom-tabs">
            <n-tab-pane name="overview" tab="Hierarchical Analysis">
              <detailedAnalysis
                :chapterScores="chapterScores"
                :results="store.results"
                class="mt-8"
              />
            </n-tab-pane>

            <n-tab-pane name="owasp" tab="OWASP Top 10 Analysis">
              <owaspAnalysis class="mt-8" />
            </n-tab-pane>

            <n-tab-pane name="impact" tab="Impact Scope Analysis">
              <impactScopeAnalysis class="mt-8" />
            </n-tab-pane>

            <n-tab-pane name="stride" tab="STRIDE Analysis">
              <strideAnalysis class="mt-8" />
            </n-tab-pane>

            <n-tab-pane name="tech" tab="Technical Impact Analysis">
              <techImpactAnalysis class="mt-8" />
            </n-tab-pane>
          </n-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from "vue";
import { useRouter } from "vue-router";
import { NProgress, NButton, NTabs, NTabPane } from "naive-ui";
import { useAssessmentStore } from "../stores/assessmentStore";
import detailedAnalysis from "../components/detailedAnalysis.vue";
import owaspAnalysis from "../components/OWASP_analysis.vue";
import impactScopeAnalysis from "../components/IS_analysis.vue";
import strideAnalysis from "../components/STRIDE_analysis.vue";
import techImpactAnalysis from "../components/TI_Analysis.vue";

const store = useAssessmentStore();
const router = useRouter();
const showDrawer = ref(false);
const detailsSection = ref(null);

const config = computed(() => store.config);
const score = computed(() => Number(store.finalReport?.soiScore) || 0);
const rating = computed(() => store.finalReport?.rating || "N/A");
const chapterScores = computed(() => {
  return store.finalReport?.aspectDetails || [];
});

const ratingColor = computed(() => {
  const s = score.value;
  if (s >= 9.0) return "text-[#63e2b7] border-[#63e2b7] bg-[#63e2b7]/10";
  if (s >= 7.0) return "text-blue-400 border-blue-400 bg-blue-400/10";
  if (s >= 4.0) return "text-yellow-500 border-yellow-500 bg-yellow-500/10";
  return "text-red-500 border-red-500 bg-red-500/10";
});

function retake() {
  store.$reset();
  router.push({ name: "Input" });
}

function openDetails() {
  // 1. Luôn đảm bảo Drawer được mở khi ấn nút này
  showDrawer.value = true;

  // 2. Đợi Vue cập nhật DOM (nextTick)
  nextTick(() => {
    const el = detailsSection.value;
    if (!el) return;

    // 3. Sử dụng scrollIntoView để cuộn
    // block: 'start' sẽ đưa đỉnh phần tử lên đầu màn hình
    el.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #63e2b7;
  border-radius: 10px;
}

:deep(.n-collapse-item-arrow) {
  color: #fff !important;
}

:deep(.n-collapse) {
  border: none !important;
}

:deep(.n-collapse-item) {
  border: none !important;
}

/* Ghi đè màu nền và viền của toàn bộ thanh Tabs */
:deep(.n-tabs.custom-tabs .n-tabs-nav) {
  background-color: transparent;
}

/* Tab trạng thái bình thường (Inactive) */
:deep(.n-tabs.custom-tabs .n-tabs-tab) {
  background-color: rgba(255, 255, 255, 0.03) !important; /* Nền tối mờ */
  color: #94a3b8 !important; /* Chữ xám xanh */
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  transition: all 0.3s ease;
  margin-right: 4px;
}

/* Tab khi di chuột qua (Hover) */
:deep(.n-tabs.custom-tabs .n-tabs-tab:hover) {
  color: #5eead4 !important;
  background-color: rgba(94, 234, 212, 0.05) !important;
}

/* Tab đang được chọn (Active) */
:deep(.n-tabs.custom-tabs .n-tabs-tab.n-tabs-tab--active) {
  background-color: #1a1a1e !important; /* Trùng với nền hoặc sáng hơn tí */
  color: #5eead4 !important; /* Chữ Xanh Mint */
  border: 1px solid #5eead4 !important; /* Viền Xanh Mint */
  font-weight: 600;
  border-bottom: 2px solid #5eead4 !important; /* Nhấn mạnh chân tab */
}

/* Xóa bỏ các đường line mặc định của Naive UI nếu cần */
:deep(.n-tabs-pad) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.n-tabs-tab-pad) {
  border: none !important;
  width: 0 !important; /* Triệt tiêu luôn khoảng cách nếu nó gây ra vạch */
}

div[ref="detailsSection"],
.min-h-screen.mt-24 {
  /* Hoặc dùng class cụ thể */
  scroll-margin-top: 40px;
}
</style>
