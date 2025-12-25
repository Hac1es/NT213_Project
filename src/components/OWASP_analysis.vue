<script setup>
import { computed, ref } from "vue";
import { useAssessmentStore } from "../stores/assessmentStore";
import owaspMapping from "../assets/OWASP_mapping.json";

// --- IMPORT VÀ ĐĂNG KÝ ECHARTS (Phải có dòng này mới hết trống) ---
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import * as echarts from "echarts/core";

// Register required ECharts components correctly (v5 modular API)
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
]);

const store = useAssessmentStore();

const owaspRiskNames = {
  A01: "Broken Access Control",
  A02: "Security Misconfiguration",
  A03: "Software Supply Chain Failures",
  A04: "Cryptographic Failures",
  A05: "Injection",
  A06: "Insecure Design",
  A07: "Authentication Failures",
  A08: "Software and Data Integrity Failures",
  A09: "Logging and Alerting Failures",
  A10: "Mishandling of Exceptional Conditions",
};

// --- LOGIC TÍNH TOÁN THEO Ý BRO (failedCount * criticality) ---
const owaspData = computed(() => {
  return Object.entries(owaspMapping).map(([riskId, data]) => {
    const requirements = data.requirements || [];
    // Normalize criticality to a number to avoid falsy/undefined showing as 0
    const critValue = Number(data.criticality ?? 0);

    // Đếm số câu bị 0 điểm
    const failedCount = requirements.filter(
      (id) => store.results?.[id] === 0
    ).length;

    // Tính điểm Score theo logic của bro
    const riskScore = failedCount * critValue;

    return {
      id: riskId,
      name: owaspRiskNames[riskId] || riskId,
      failedCount,
      criticality: critValue,
      score: riskScore,
    };
  });
});

// Sắp xếp rủi ro cho bảng (Rank)
const rankedOWASPRisks = computed(() => {
  return [...owaspData.value].sort((a, b) => b.score - a.score);
});

// --- CẤU HÌNH BIỂU ĐỒ (Dùng dữ liệu đồng bộ ở trên) ---
const chartOption = computed(() => {
  const data = owaspData.value;
  return {
    backgroundColor: "transparent",
    tooltip: { trigger: "axis", axisPointer: { type: "cross" } },
    legend: { textStyle: { color: "#888" }, bottom: 0 },
    grid: { left: "3%", right: "4%", bottom: "15%", containLabel: true },
    xAxis: {
      type: "category",
      data: data.map((d) => d.id),
      axisLabel: { color: "#666", fontWeight: "bold" },
    },
    yAxis: [
      {
        type: "value",
        name: "Failures",
        splitLine: { lineStyle: { color: "#222" } },
        axisLabel: { color: "#FF0054" },
      },
      {
        type: "value",
        name: "Risk Score",
        splitLine: { show: false },
        axisLabel: { color: "#00F5D4" },
      },
    ],
    series: [
      {
        name: "CWE Count (Failures)",
        type: "bar",
        barMaxWidth: 15,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#FF0054" },
            { offset: 1, color: "#80002A" },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        data: data.map((d) => d.failedCount),
      },
      {
        name: "Risk Score (Count * Crit)",
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: { color: "#00F5D4", width: 3 },
        itemStyle: { color: "#fff", borderColor: "#00F5D4", borderWidth: 2 },
        data: data.map((d) => d.score.toFixed(2)),
      },
    ],
  };
});
</script>

<template>
  <div class="space-y-8 mt-8">
    <h2 class="text-[#63e2b7] text-4xl font-black mb-8 tracking-tighter">
      Security Risk Summary
    </h2>

    <div
      class="bg-[#14161B] p-6 rounded-2xl border border-white/5 shadow-2xl h-[450px]"
    >
      <v-chart :option="chartOption" autoresize />
    </div>

    <div class="bg-[#14161B] border border-white/5 rounded-2xl overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-gray-500 uppercase text-[10px] tracking-[0.2em] border-b border-gray-800/50 bg-white/[0.02]"
          >
            <th class="p-5 font-black">Security Risk</th>
            <th class="p-5 font-black text-center">Number of CWEs</th>
            <th class="p-5 font-black text-center">Criticality</th>
            <th class="p-5 font-black text-center">Score</th>
            <th class="p-5 font-black text-center">Rank</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(risk, idx) in rankedOWASPRisks"
            :key="risk.id"
            class="hover:bg-white/[0.01]"
          >
            <td class="p-5">
              <span class="text-gray-200 font-bold text-sm"
                >{{ risk.id }} - {{ risk.name }}</span
              >
            </td>
            <td class="p-5 text-center">
              <span class="font-mono text-[#63e2b7]">{{
                risk.failedCount
              }}</span>
            </td>
            <td class="p-5 text-center">
              <span class="font-mono text-gray-400">{{
                risk.criticality
              }}</span>
            </td>
            <td class="p-5 text-center">
              <span
                class="font-mono font-bold"
                :class="risk.score >= 1.5 ? 'text-red-500' : 'text-green-500'"
              >
                {{ risk.score.toFixed(2) }}
              </span>
            </td>
            <td class="p-5 text-center">
              <span
                class="inline-block px-3 py-1 rounded-full font-black text-[10px] bg-gray-800 text-gray-400"
              >
                TOP {{ idx + 1 }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
