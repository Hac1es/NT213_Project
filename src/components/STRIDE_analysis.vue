<template>
  <div>
    <h2 class="text-[#63e2b7] text-3xl font-black mb-3 tracking-tighter">
      Security Risk Summary
    </h2>

    <h2 class="text-gray-400 text-lg font-black mb-8 tracking-tighter">
      Based on STRIDE Threat Model
    </h2>

    <v-chart
      class="w-full"
      style="height: 400px"
      :option="getChartOption(strideData)"
      autoresize
    />

    <div class="overflow-x-auto p-6 rounded-2xl mt-5">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-gray-400 uppercase text-xs tracking-widest border-b border-gray-700"
          >
            <th class="pb-4 font-black">Threat Category</th>
            <th class="pb-4 font-black text-center">Number of CWEs</th>
            <th class="pb-4 font-black text-center">Rank</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-800/30">
          <tr
            v-for="(item, idx) in rankedStride"
            :key="item.name"
            class="hover:bg-white/5"
          >
            <td class="py-4">
              <span class="text-gray-200 font-bold">{{ item.name }}</span>
            </td>
            <td class="py-4 text-center">
              <span class="font-mono text-[#63e2b7] text-lg font-bold">{{
                item.failedCount
              }}</span>
            </td>
            <td class="py-4 text-center">
              <span
                class="inline-block px-3 py-1 rounded-full font-bold text-xs"
                :class="
                  idx === 0
                    ? 'bg-red-500/20 text-red-400'
                    : idx === 1
                    ? 'bg-orange-500/20 text-orange-400'
                    : idx === 2
                    ? 'bg-yellow-500/20 text-yellow-400'
                    : 'bg-gray-600/20 text-gray-400'
                "
              >
                {{ idx + 1 }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAssessmentStore } from "../stores/assessmentStore";
import strideMapping from "../assets/stride_mapping.json";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import * as echarts from "echarts/core";

use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
]);

const store = useAssessmentStore();

const strideData = computed(() => {
  return Object.entries(strideMapping).map(([name, requirements]) => {
    const failedCount = requirements.filter(
      (reqId) => store.results?.[reqId] === 0
    ).length;
    return { name, failedCount };
  });
});

const rankedStride = computed(() => {
  return [...strideData.value].sort((a, b) => b.failedCount - a.failedCount);
});

const getChartOption = (data) => {
  return {
    backgroundColor: "transparent",
    tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
    legend: { textStyle: { color: "#888" }, bottom: 0 },
    grid: { left: "3%", right: "4%", bottom: "15%", containLabel: true },
    xAxis: {
      type: "category",
      data: data.map((d) => d.name),
      axisLabel: { color: "#666", fontWeight: "bold", rotate: 45 },
    },
    yAxis: {
      type: "value",
      name: "Failed ASVS Count",
      splitLine: { lineStyle: { color: "#222" } },
      axisLabel: { color: "#FF0054" },
    },
    series: [
      {
        name: "Failed Requirements",
        type: "bar",
        barMaxWidth: 75,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#FF0054" },
            { offset: 1, color: "#80002A" },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        data: data.map((d) => d.failedCount),
      },
    ],
  };
};
</script>
