<template>
  <div class="h-full w-[80%] mx-auto flex flex-col justify-center">
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-bold mb-2 text-[#63e2b7]">How It Works</h1>
      <p class="text-gray-400 text-xl">
        Three simple steps to quantify your application security.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div
        class="bg-[#18181c] border border-gray-700 rounded-lg p-6 relative overflow-hidden flex flex-col"
      >
        <div class="absolute top-0 left-0 w-full h-1 bg-[#63e2b7]"></div>
        <div class="mb-4 text-[#63e2b7]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-10 w-10"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-white mb-2">1. Setup Context</h3>
        <p class="text-gray-400 text-lg flex-grow">
          Provide auditor details and target application information. Select the
          appropriate ASVS Level
          <span class="font-semibold text-white"
            >(Level 1, Level 2, or Level 3)</span
          >
          based on your app's risk profile.
        </p>
      </div>

      <div
        class="bg-[#18181c] border border-gray-700 rounded-lg p-6 relative overflow-hidden flex flex-col md:-mt-4 md:shadow-[0_0_20px_rgba(99,226,183,0.15)] z-10"
      >
        <div class="absolute top-0 left-0 w-full h-1 bg-[#63e2b7]"></div>
        <div class="absolute top-0 left-0 w-1 h-full bg-[#63e2b7]"></div>
        <div class="mb-4 text-[#63e2b7]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-10 w-10"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-white mb-2">2. Evaluate Controls</h3>
        <p class="text-gray-300 text-lg mb-4">
          Go through the checklist and assign scores
          <span class="font-serif italic"> 0, 0.5, 1 </span>.
        </p>

        <div class="mt-auto p-3 bg-[#101014]/80 rounded border border-gray-800">
          <span
            class="text-base font-bold text-gray-500 uppercase tracking-wide"
            >Crucial Rule:</span
          >
          <p class="text-base text-gray-400 leading-snug">
            If a mechanism is not feasible due to technical constraints, leave
            it
            <span class="text-white font-bold border-b border-gray-500"
              >unchecked</span
            >. The system will treat it as <strong>N/A</strong> and exclude it
            from calculations.
          </p>
        </div>
      </div>

      <div
        class="bg-[#18181c] border border-gray-700 rounded-lg p-6 relative overflow-hidden flex flex-col"
      >
        <div class="absolute top-0 left-0 w-full h-1 bg-[#63e2b7]"></div>

        <div class="mb-4 text-[#63e2b7]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-10 w-10"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"
            />
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-white mb-2">3. Analyze Results</h3>
        <p class="text-gray-400 text-lg flex-grow">
          Review the generated scorecard and domain-specific charts to identify
          strengths and prioritize remediations effectively.
        </p>
      </div>
    </div>

    <div class="text-center">
      <RouterLink
        to="/input"
        class="px-10 py-4 bg-[#63e2b7] hover:bg-[#4fd1a8] text-[#101014] text-xl font-bold rounded transition-all shadow-[0_0_15px_rgba(99,226,183,0.4)] hover:shadow-[0_0_25px_rgba(99,226,183,0.6)] active:scale-95"
      >
        Start Assessment
      </RouterLink>
    </div>
  </div>
</template>
