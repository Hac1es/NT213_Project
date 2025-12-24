<template>
  <div>
    <h2 class="text-[#63e2b7] text-3xl font-black">Technical Impact Summary</h2>

    <v-chart
      class="w-full"
      style="height: 1500px"
      :option="getChartOption(techImpactData)"
      autoresize
    />

    <div class="overflow-x-auto p-6 rounded-2xl mt-5">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-gray-400 uppercase text-xs tracking-widest border-b border-gray-700"
          >
            <th class="pb-4 font-black">Technical Impact</th>
            <th class="pb-4 font-black text-center">Number of CWEs</th>
            <th class="pb-4 font-black text-center">Rank</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-800/30">
          <tr
            v-for="(item, idx) in rankedTechImpact"
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
import techImpactMapping from "../assets/technical_impact_mapping.json";
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

const techImpactData = computed(() => {
  return Object.entries(techImpactMapping).map(([name, requirements]) => {
    const failedCount = requirements.filter(
      (reqId) => store.results?.[reqId] === 0
    ).length;
    return { name, failedCount };
  });
});

const rankedTechImpact = computed(() => {
  return [...techImpactData.value].sort(
    (a, b) => b.failedCount - a.failedCount
  );
});

const getChartOption = (data) => {
  return {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
    },
    legend: { textStyle: { color: "#888" }, bottom: 0 },
    // Căn chỉnh lề trái rộng ra một chút để không bị mất chữ Technical Impact
    grid: {
      left: "5%",
      right: "8%",
      bottom: "10%",
      top: "5%",
      containLabel: true,
    },

    // TRỤC X: Giờ đóng vai trò là trục Giá trị (Value)
    xAxis: {
      type: "value",
      name: "Failed ASVS",
      nameTextStyle: { color: "#666" },
      splitLine: { lineStyle: { color: "#222" } },
      axisLabel: { color: "#666" },
    },

    // TRỤC Y: Giờ đóng vai trò là trục Nhãn (Category)
    yAxis: {
      type: "category",
      data: data.map((d) => d.name), // Đưa list tên TI vào đây
      axisLabel: {
        color: "#ccc",
        fontWeight: "bold",
        fontSize: 11,
        // Nếu tên dài quá có thể giới hạn độ dài ở đây
        formatter: (value) =>
          value.length > 25 ? value.slice(0, 25) + "..." : value,
      },
      axisLine: { lineStyle: { color: "#444" } },
    },

    series: [
      {
        name: "Failed Requirements",
        type: "bar",
        barMaxWidth: 20,
        itemStyle: {
          // Gradient đổi thành từ trái sang phải (0, 0, 1, 0)
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: "#80002A" },
            { offset: 1, color: "#FF0054" },
          ]),
          // Bo góc bên phải của thanh bar [top-left, top-right, bottom-right, bottom-left]
          borderRadius: [0, 4, 4, 0],
        },
        data: data.map((d) => d.failedCount),
      },
    ],
  };
};
</script>
