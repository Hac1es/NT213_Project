<script setup>
import { computed } from "vue";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, ScatterChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";

use([
  CanvasRenderer,
  BarChart,
  ScatterChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
]);

// Props
const props = defineProps({
  aspectData: {
    type: Array,
    required: true,
    description: "Array of aspect objects with criteriaDetails and counts",
  },
  level: {
    type: Number,
    default: 1,
  },
});

// Computed
const chapterScores = computed(() => props.aspectData || []);

// Hàm tạo option cho từng Aspect
const getChartOption = (aspectData) => {
  const criteriaNames = aspectData.criteriaDetails.map((c) => c.name);

  return {
    backgroundColor: "transparent",
    tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
    legend: { textStyle: { color: "#ccc" }, bottom: 0 },
    grid: { left: "3%", right: "4%", bottom: "15%", containLabel: true },
    xAxis: {
      type: "category",
      data: criteriaNames,
      axisLabel: { color: "#888", rotate: 45 },
    },
    yAxis: [
      { type: "value", name: "Quantity", axisLabel: { color: "#888" } },
      {
        type: "value",
        name: "Score",
        min: 0,
        max: 1,
        axisLabel: { color: "#94A3B8" },
      },
    ],
    series: [
      {
        name: "Pass (1.0)",
        type: "bar",
        stack: "total",
        color: "#10B981", // XANH
        barMaxWidth: 100,
        data: aspectData.criteriaDetails.map((c) => c.counts.pass),
      },
      {
        name: "Partial (0.5)",
        type: "bar",
        stack: "total",
        color: "#F59E0B", // VÀNG
        barMaxWidth: 100,
        data: aspectData.criteriaDetails.map((c) => c.counts.partial),
      },
      {
        name: "Fail (0)",
        type: "bar",
        stack: "total",
        color: "#EF4444", // ĐỎ
        barMaxWidth: 100,
        data: aspectData.criteriaDetails.map((c) => c.counts.fail),
      },
      {
        name: "Average Score",
        type: "scatter",
        yAxisIndex: 1,
        symbolSize: 12,
        color: "#fff", // DẤU CHẤM TRẮNG
        itemStyle: { borderColor: "#63e2b7", borderWidth: 2 },
        data: aspectData.criteriaDetails.map((c) => c.score.toFixed(2)),
      },
    ],
  };
};
</script>

<template>
  <div class="space-y-12 w-full">
    <div v-for="aspect in chapterScores" :key="aspect.aspect" class="mt-6">
      <!-- Empty state when no criteria data -->
      <div
        v-if="!aspect.criteriaDetails || aspect.criteriaDetails.length === 0"
        class="flex flex-col items-center justify-center py-16 px-8 border border-dashed border-gray-700 rounded-xl bg-[#18181c]/50"
      >
        <svg
          class="w-12 h-12 text-gray-600 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <p class="text-gray-400 text-center font-medium">
          No requirements for this aspect at
          <span class="text-[#63e2b7] font-bold">Level {{ level }}</span>
        </p>
        <p class="text-gray-600 text-sm mt-2">
          Try selecting a higher verification level to see data.
        </p>
      </div>

      <!-- Chart when data exists -->
      <div v-else style="width: 100%; height: 550px">
        <v-chart :option="getChartOption(aspect)" autoresize />
      </div>
    </div>
  </div>
</template>
