<template>
  <div
    class="min-h-screen flex flex-col items-start justify-start bg-[#101014] text-white py-10"
  >
    <div class="w-[80%] mx-auto mb-12">
      <h1 class="text-4xl font-bold mb-2 text-[#63e2b7]">
        New Security Assessment
      </h1>
      <p class="text-gray-400 mb-5 text-xl">
        OWASP ASVS 4.0.3 Quantitative Evaluation Model
      </p>

      <div class="grid grid-cols-2 gap-6 mb-5">
        <div class="flex flex-col gap-2">
          <label class="text-gray-400 text-xl">Target Application</label>
          <input
            v-model="assessmentData.targetApp"
            type="text"
            placeholder="e.g. My App v1.0"
            class="bg-[#18181c] text-xl border border-gray-700 rounded p-3 text-white focus:border-[#63e2b7] focus:outline-none transition"
          />
        </div>
        <div class="flex flex-col gap-2">
          <label class="text-xl text-gray-400">Auditor Name</label>
          <input
            v-model="assessmentData.auditorName"
            type="text"
            placeholder="e.g. John Doe"
            class="bg-[#18181c] text-xl border border-gray-700 rounded p-3 text-white focus:border-[#63e2b7] focus:outline-none transition"
          />
        </div>
      </div>

      <div class="mb-5">
        <label class="text-gray-400 text-xl block mb-4"
          >Verification Level</label
        >
        <div class="grid grid-cols-3 gap-6">
          <div
            v-for="level in [1, 2, 3]"
            :key="level"
            @click="assessmentData.level = level"
            :class="[
              'bg-[#18181c] border-2 p-5 rounded-lg cursor-pointer transition-all duration-300 relative overflow-hidden group',
              assessmentData.level === level
                ? 'border-[#63e2b7] shadow-[0_0_15px_rgba(99,226,183,0.2)]'
                : 'border-gray-700 hover:border-gray-500',
            ]"
          >
            <div
              v-if="assessmentData.level === level"
              class="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#63e2b7] animate-pulse"
            ></div>

            <h4
              :class="[
                'text-2xl font-bold mb-2',
                assessmentData.level === level
                  ? 'text-[#63e2b7]'
                  : 'text-white',
              ]"
            >
              Level {{ level }}
            </h4>
            <p class="text-gray-400 text-sm leading-snug">
              {{ levelDescriptions[level] }}
            </p>
          </div>
        </div>
      </div>

      <div
        class="bg-[#18181c] border border-gray-700 rounded-lg p-6 relative overflow-hidden mb-10"
      >
        <div class="absolute top-0 left-0 w-1 h-full bg-[#63e2b7]"></div>
        <h3
          class="text-xl font-semibold text-white mb-2 flex items-center gap-2"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 text-[#63e2b7]"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          Evaluation Guidelines
        </h3>
        <p class="text-gray-300 text-lg leading-relaxed">
          The ASVS standard covers a wide range of security controls. It is
          important to note that
          <span class="text-white font-medium"
            >due to the specific technologies used in your software, some
            mechanisms may not be feasible or applicable.</span
          >
        </p>
        <div
          class="mt-4 flex items-center gap-3 p-3 bg-[#101014]/50 rounded border border-gray-800"
        >
          <span class="text-lg font-bold text-gray-500 uppercase tracking-wide"
            >Action:</span
          >
          <p class="text-lg text-gray-400">
            Simply leave these items
            <span class="text-white font-bold border-b border-gray-500"
              >unchecked</span
            >. The system will automatically treat them as
            <strong>N/A</strong> and exclude them from calculations.
          </p>
        </div>
      </div>

      <div class="flex justify-center w-full mt-8">
        <button
          @click="handleStart"
          class="w-full py-3 bg-[#63e2b7] text-[#101014] font-bold text-lg rounded hover:bg-[#4fd1a8] transition-all shadow-[0_0_15px_rgba(99,226,183,0.3)] active:scale-[0.98]"
        >
          Start Assessment
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router"; // Thêm router

const router = useRouter();

const emit = defineEmits(["start-assessment"]);

// Dữ liệu đánh giá
const assessmentData = reactive({
  targetApp: "",
  auditorName: "",
  level: 1, // Mặc định là Level 1
});

// Mô tả cho từng Level dựa trên tiêu chuẩn ASVS
const levelDescriptions = {
  1: "Basic security requirements. Suitable for all applications where low confidence is required.",
  2: "Standard security controls for applications handling sensitive B2B or consumer data.",
  3: "Advanced security for critical applications (Financial, Medical, or Critical Infrastructure).",
};

// Hàm xử lý khi nhấn Start
function handleStart() {
  if (!assessmentData.targetApp || !assessmentData.auditorName) {
    alert("Please fill in all fields before starting.");
    return;
  }

  // Điều hướng bằng query thay vì params để tránh lỗi "Missing param"
  // và giúp URL dễ đọc hơn khi người dùng nhấn Back/Forward
  router.push({
    name: "Main",
    query: {
      targetApp: assessmentData.targetApp,
      auditorName: assessmentData.auditorName,
      level: assessmentData.level,
    },
  });
}
</script>
