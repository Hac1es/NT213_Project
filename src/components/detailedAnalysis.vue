<template>
  <div>
    <h1 class="text-[#63e2b7] text-3xl font-black">
      Detailed Hierarchical Analysis
    </h1>
    <div class="space-y-8 mt-6">
      <div v-for="aspect in chapterScores" :key="aspect.aspect">
        <p
          class="text-[#10b981] font-bold text-lg mb-2 flex items-center gap-2 uppercase tracking-tight"
        >
          {{ aspect.aspect }}
        </p>
        <mainChart :aspectData="[aspect]" class="mb-6" />
        <n-collapse arrow-placement="right">
          <n-collapse-item
            v-for="(crit, index) in aspect.criteriaDetails"
            :key="crit.name"
            :title="crit.name"
            :name="crit.name"
          >
            <template #header>
              <div class="flex-1 min-w-0">
                <span class="text-[#99F6E4] text-base font-bold truncate">{{
                  crit.name
                }}</span>
              </div>
            </template>

            <template #header-extra>
              <span
                class="font-mono text-base font-bold shrink-0"
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
              >
                <template #header>
                  <div class="flex-1 min-w-0">
                    <span class="text-[#CBD5E1] text-sm font-bold truncate">{{
                      elem.name
                    }}</span>
                  </div>
                </template>
                <template #header-extra>
                  <span
                    class="text-sm font-mono font-bold shrink-0"
                    :class="
                      elem.score >= 0.695 ? 'text-green-500' : 'text-red-500'
                    "
                  >
                    {{ elem.score.toFixed(2) }}
                  </span>
                </template>

                <!-- Mechanism level collapse inside element -->
                <n-collapse arrow-placement="right">
                  <n-collapse-item
                    v-for="mech in elem.mechanismsDetails"
                    :key="mech.name"
                    :title="mech.name"
                    :name="mech.name"
                  >
                    <template #header>
                      <div class="flex-1 min-w-0">
                        <span
                          class="text-[#94A3B8] text-xs font-bold truncate"
                          >{{ mech.name }}</span
                        >
                      </div>
                    </template>
                    <template #header-extra>
                      <span
                        class="text-xs font-mono font-bold shrink-0"
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

<style scoped>
/* --- 1. TRIỆT TIÊU TOÀN BỘ BORDER MẶC ĐỊNH --- */
:deep(.n-collapse) {
  --n-item-margin: 0 !important;
  --n-title-padding: 0 !important;
  /* Xóa màu kẻ ngang mặc định của Naive UI */
  --n-divider-color: transparent !important;
}

/* Xóa border của chính thẻ collapse-item */
:deep(.n-collapse-item) {
  border: none !important;
}

/* San phẳng & Xóa đường kẻ dọc phân cấp */
:deep(.n-collapse .n-collapse) {
  margin-left: 0 !important;
  padding-left: 0 !important;
  border-left: none !important; /* XÓA ĐƯỜNG KẺ DỌC */
}

/* --- 2. LAYOUT: TIÊU ĐỀ -> MŨI TÊN ... ĐIỂM SỐ --- */

:deep(.n-collapse-item__header) {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 12px 0 !important;
  /* XÓA ĐƯỜNG KẺ NGANG DƯỚI HEADER */
  border-bottom: none !important;
}

/* Khối bên trái: Tiêu đề + Mũi tên */
:deep(.n-collapse-item__header-main) {
  display: flex !important;
  align-items: center !important;
  flex: 1 !important;
  min-width: 0 !important;
}

/* Mũi tên nằm sát sau tiêu đề */
:deep(.n-collapse-item-arrow) {
  margin-left: 8px !important;
  flex-shrink: 0 !important;
}

/* Khối bên phải: Điểm số */
:deep(.n-collapse-item__header-extra) {
  margin-left: auto !important;
  padding-left: 20px !important;
  flex-shrink: 0 !important;
}

/* --- 3. FIX CHI TIẾT CONTENT --- */

:deep(.n-collapse-item__content-inner) {
  padding-left: 0 !important;
  padding-top: 8px !important;
  padding-bottom: 20px !important;
  /* Đảm bảo nội dung không tự đẻ ra border top */
  border-top: none !important;
}
</style>
