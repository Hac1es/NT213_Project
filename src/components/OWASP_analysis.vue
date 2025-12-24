<template>
  <div>
    <h2 class="text-[#63e2b7] text-4xl font-black mb-3">
      Security Risk Summary
    </h2>

    <p class="text-gray-400 text-lg font-black mb-8">
      Based on OWASP Top 10 (2025)
    </p>

    <v-chart
      class="w-full"
      style="height: 400px"
      :option="getOWASPChartOption(owaspData)"
      autoresize
    />

    <div class="overflow-x-auto p-6 rounded-2xl mt-5">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-gray-400 uppercase text-xs tracking-widest border-b border-gray-700"
          >
            <th class="pb-4 font-black">Security Risk</th>
            <th class="pb-4 font-black text-center">Number of CWEs</th>
            <th class="pb-4 font-black text-center">Criticality</th>
            <th class="pb-4 font-black text-center">Score</th>
            <th class="pb-4 font-black text-center">Rank</th>
          </tr>
        </thead>

        <tbody class="divide-y divide-gray-800/30">
          <tr
            v-for="(risk, idx) in rankedOWASPRisks"
            :key="risk.id"
            class="hover:bg-white/5"
          >
            <td class="py-4">
              <span class="text-gray-200 font-bold">
                {{ risk.id }} - {{ risk.name }}
              </span>
            </td>
            <td class="py-4 text-center">
              <span class="font-mono text-[#63e2b7]">{{
                risk.failedCount
              }}</span>
            </td>
            <td class="py-4 text-center">
              <span class="font-mono text-gray-400">{{
                risk.criticality
              }}</span>
            </td>
            <td class="py-4 text-center">
              <span
                class="font-mono font-bold"
                :class="
                  risk.score >= 1.5
                    ? 'text-red-500'
                    : risk.score >= 0.8
                    ? 'text-yellow-500'
                    : 'text-green-500'
                "
              >
                {{ risk.score.toFixed(2) }}
              </span>
            </td>
            <td class="py-4 text-center">
              <span
                class="inline-block px-3 py-1 rounded-full font-bold text-sm"
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
import owaspMapping from "../assets/OWASP_mapping.json";
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

const owaspData = computed(() => {
  return Object.entries(owaspMapping).map(([riskId, data]) => {
    const requirements = data.requirements || [];
    const critValue = Number(data.criticality ?? 0);
    const failedCount = requirements.filter(
      (reqId) => store.results?.[reqId] === 0
    ).length;
    const score = failedCount * critValue;

    return {
      id: riskId,
      name: owaspRiskNames[riskId] || riskId,
      failedCount,
      criticality: critValue,
      score,
    };
  });
});

const rankedOWASPRisks = computed(() => {
  return [...owaspData.value].sort((a, b) => b.score - a.score);
});

const getOWASPChartOption = (data) => {
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
        barMaxWidth: 20,
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
        name: "Risk Score",
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        symbolSize: 8,
        lineStyle: {
          color: "#00F5D4",
          width: 3,
          shadowBlur: 10,
          shadowColor: "rgba(0,245,212,0.5)",
        },
        itemStyle: { color: "#fff", borderColor: "#00F5D4", borderWidth: 2 },
        data: data.map((d) => d.score.toFixed(2)),
      },
    ],
  };
};
</script>
