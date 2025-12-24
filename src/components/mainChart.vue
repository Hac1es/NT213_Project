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
    <div v-for="aspect in chapterScores" :key="aspect.aspect">
      <div style="width: 100%; height: 700px">
        <v-chart :option="getChartOption(aspect)" autoresize />
      </div>
    </div>
  </div>
</template>
