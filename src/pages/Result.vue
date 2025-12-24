<template>
  <div class="min-h-screen bg-[#101014] text-white py-12">
    <div class="w-[80%] mx-auto">
      <div
        class="flex justify-between items-end mb-12 border-b border-gray-800 pb-8"
      >
        <div>
          <h1 class="text-[#63e2b7] text-4xl font-black mb-2">FINAL REPORT</h1>
          <p class="text-gray-400 text-lg italic">
            Quantitative assessment for
            <span class="text-white font-bold">{{ config.targetApp }}</span>
          </p>
        </div>
        <div class="text-right text-white text-lg font-mono">
          <p>Auditor: {{ config.auditorName }}</p>
          <p>ASVS Level: {{ config.level }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        <div
          class="p-8 rounded-3xl border border-[#63e2b7]/20 flex flex-col items-center justify-center relative overflow-hidden shadow-2xl"
        >
          <div
            class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#63e2b7] to-transparent"
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
                  class="group transition-colors hover:bg-white/[0.02]"
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
          class="h-12 font-semibold border border-[#2E3235] hover:(bg-[#1F2224] border-[#63E2B7] text-[#6AF5B3]) shadow-[inset_0_0_12px_#0D1512,0_0_6px_#0D1512] transition-all duration-300"
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
          @click="showDrawer = !showDrawer"
        >
          GET DETAILS
        </n-button>
      </div>

      <div class="mt-32" v-show="showDrawer">
        <h1 class="text-[#63e2b7] text-4xl font-black">
          Detailed Hierarchical Analysis
        </h1>
        <div class="space-y-8 mt-6">
          <div v-for="aspect in chapterScores" :key="aspect.aspect">
            <h3
              class="text-[#10b981] font-bold text-xl mb-4 flex items-center gap-2 uppercase tracking-tight"
            >
              {{ aspect.aspect }}
            </h3>
            <mainChart :aspectData="[aspect]" class="mb-6" />
            <n-collapse arrow-placement="right">
              <n-collapse-item
                v-for="(crit, index) in aspect.criteriaDetails"
                :key="crit.name"
                :title="crit.name"
                :name="crit.name"
              >
                <template #header>
                  <span class="text-[#99F6E4] text-lg font-bold">{{
                    crit.name
                  }}</span>
                </template>

                <template #header-extra>
                  <span
                    class="text-lg font-mono font-bold"
                    :class="
                      crit.score >= 0.695 ? 'text-green-500' : 'text-red-500'
                    "
                    >{{ crit.score.toFixed(2) }}</span
                  >
                </template>
                <!-- Element level collapse -->
                <n-collapse arrow-placement="right">
                  <n-collapse-item
                    v-for="elem in crit.elementsDetails"
                    :key="elem.name"
                    :title="elem.name"
                    :name="elem.name"
                    class="py-1"
                  >
                    <template #header>
                      <span class="text-[#CBD5E1] text-base font-bold">{{
                        elem.name
                      }}</span>
                    </template>
                    <template #header-extra>
                      <span
                        class="text-base font-mono font-bold"
                        :class="
                          elem.score >= 0.695
                            ? 'text-green-500'
                            : 'text-red-500'
                        "
                      >
                        {{ elem.score.toFixed(2) }}
                      </span>
                    </template>

                    <!-- Mechanism level collapse inside element -->
                    <n-collapse arrow-placement="right" class="ml-2">
                      <n-collapse-item
                        v-for="mech in elem.mechanismsDetails"
                        :key="mech.name"
                        :title="mech.name"
                        :name="mech.name"
                      >
                        <template #header>
                          <span class="text-[#94A3B8] text-sm font-bold">{{
                            mech.name
                          }}</span>
                        </template>
                        <template #header-extra>
                          <span
                            class="text-sm font-mono font-bold"
                            :class="
                              mech.score >= 0.695
                                ? 'text-green-500'
                                : 'text-red-500'
                            "
                          >
                            {{
                              mech.score != null ? mech.score.toFixed(2) : "N/A"
                            }}
                          </span>
                        </template>

                        <!-- ASVS requirement tags inside mechanism -->
                        <div class="flex flex-wrap gap-2 py-1">
                          <n-tag
                            v-for="rid in mech.requirements"
                            :key="rid"
                            size="small"
                            round
                            :color="getTagColor(getReqScore(rid))"
                          >
                            {{ rid }}
                            <span class="ml-1 opacity-70"
                              >({{ getReqScore(rid) ?? "N/A" }})</span
                            >
                          </n-tag>
                        </div>
                      </n-collapse-item>
                    </n-collapse>
                  </n-collapse-item>
                </n-collapse>
              </n-collapse-item>
            </n-collapse>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  NProgress,
  NButton,
  NDrawer,
  NDrawerContent,
  NCollapse,
  NCollapseItem,
  NTag,
} from "naive-ui";
import { useAssessmentStore } from "../stores/assessmentStore";
import asvsData from "../assets/asvsData.json";
import mainChart from "../components/mainChart.vue";

const store = useAssessmentStore();
const route = useRoute();
const router = useRouter();
const showDrawer = ref(false);

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

// Helpers for mechanism -> requirement drilldown
const reqMap = computed(() => {
  const map = {};
  try {
    asvsData.forEach((chapter) => {
      (chapter.requirements || []).forEach((r) => {
        map[r.id] = r.text;
      });
    });
  } catch (e) {}
  return map;
});

function getReqScore(id) {
  const v = store.results?.[id];
  return typeof v === "number" ? v : null;
}

const getTagColor = (s) => {
  const map = {
    1: {
      color: "rgba(74, 222, 128, 0.1)",
      textColor: "#4ADE80",
      borderColor: "rgba(74, 222, 128, 0.2)",
    },
    0.5: {
      color: "rgba(253, 224, 71, 0.1)", // vàng
      textColor: "#FACC15",
      borderColor: "rgba(253, 224, 71, 0.25)",
    },
    0: {
      color: "rgba(248, 113, 113, 0.1)",
      textColor: "#F87171",
      borderColor: "rgba(248, 113, 113, 0.2)",
    },
  };

  return map[s] ?? map[0];
};
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
</style>
