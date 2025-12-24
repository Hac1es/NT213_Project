<template>
  <div>
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
                :class="crit.score >= 0.695 ? 'text-green-500' : 'text-red-500'"
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
                      elem.score >= 0.695 ? 'text-green-500' : 'text-red-500'
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
                        {{ mech.score != null ? mech.score.toFixed(2) : "N/A" }}
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
</template>

<script setup>
import { NCollapse, NCollapseItem, NTag } from "naive-ui";
import mainChart from "./mainChart.vue";

// Properly capture props in <script setup>
const props = defineProps({
  chapterScores: {
    type: Array,
    required: true,
  },
  results: {
    type: Object,
    default: () => ({}),
  },
});

function getReqScore(id) {
  const v = props.results?.[id];
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
      color: "rgba(253, 224, 71, 0.1)",
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
