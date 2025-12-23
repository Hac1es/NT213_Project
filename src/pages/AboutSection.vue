<template>
  <div class="h-full w-[80%] mx-auto flex flex-col justify-center">
    <div class="mb-12">
      <h1 class="text-4xl font-bold mb-2 text-[#63e2b7]">
        More Than Just a Checklist
      </h1>
      <p class="text-gray-400 text-xl">
        Bridging the gap between qualitative ASVS requirements and quantitative
        metrics.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
      <div class="space-y-8">
        <div>
          <h3
            class="text-2xl font-semibold text-white mb-3 flex items-center gap-2"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-[#63e2b7]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            The Problem
          </h3>
          <p class="text-gray-300 text-lg leading-relaxed">
            Traditional security assessments often result in lengthy PDFs.
            Knowing you passed 150 requirements and failed 20 doesn't tell you
            <span class="text-white font-medium">how secure</span> your
            application actually is, or where the critical weaknesses lie across
            different domains.
          </p>
        </div>

        <div>
          <h3
            class="text-2xl font-semibold text-white mb-3 flex items-center gap-2"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-[#63e2b7]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
              />
            </svg>
            The Quantitative Solution
          </h3>
          <p class="text-gray-300 text-lg leading-relaxed">
            Based on academic research, Q-ASVS transforms generic checklists
            into a mathematical model. By assigning weighted scores<span
              class="font-serif italic"
            >
              0, 0.5, 1 </span
            >, we provide actionable insights and tangible security scores that
            are easy to track over time.
          </p>
        </div>
      </div>

      <div
        class="bg-[#18181c] border border-gray-700 rounded-lg p-6 relative overflow-hidden shadow-lg"
      >
        <div class="absolute top-0 left-0 w-1 h-full bg-[#63e2b7]"></div>

        <h3
          class="text-xl font-semibold text-white mb-6 flex items-center gap-2"
        >
          Visualized Security Posture
        </h3>

        <div class="space-y-4">
          <div
            class="flex justify-between items-center p-3 bg-[#101014]/50 rounded border border-gray-800"
          >
            <span class="text-gray-400 text-lg">Software Structure</span>
            <span class="text-[#63e2b7] font-bold text-xl">0.45</span>
          </div>
          <div
            class="flex justify-between items-center p-3 bg-[#101014]/50 rounded border border-gray-800"
          >
            <span class="text-gray-400 text-lg">Software Environment</span>
            <span class="text-yellow-500 font-bold text-xl">0.26</span>
          </div>
          <div
            class="flex justify-between items-center p-3 bg-[#101014]/50 rounded border border-gray-800"
          >
            <span class="text-gray-400 text-lg">Software Process</span>
            <span class="text-red-500 font-bold text-xl">0.06</span>
          </div>
        </div>

        <p class="mt-4 text-gray-500 text-sm text-center">
          *Illustrative data meant to show scoring potential.
        </p>
      </div>
    </div>

    <div class="mt-16 flex justify-center">
      <button
        @click="$emit('next')"
        class="group flex items-center gap-2 text-[#63e2b7] text-lg font-semibold hover:text-white transition-colors duration-300"
      >
        See How It Works
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 group-hover:translate-y-1 transition-transform"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
// Emits event để component cha (App.vue) biết khi nào cần cuộn xuống
defineEmits(["next"]);
</script>
