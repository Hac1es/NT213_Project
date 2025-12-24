<template>
  <div
    class="w-full flex flex-col gap-3 mt-6 border-b border-gray-800/60 pb-6 last:border-0"
  >
    <div class="flex gap-4 w-full text-white items-baseline">
      <span class="font-bold text-[#63e2b7] shrink-0 min-w-17.5 text-xl">
        {{ heading }}
      </span>

      <div class="flex-1 min-w-0 flex flex-col gap-2">
        <span class="wrap-break-word text-gray-200 leading-relaxed text-lg">
          {{ title }}
        </span>
      </div>
    </div>

    <div class="flex gap-3 mt-2 pl-22">
      <n-button
        @click="handleClick(0)"
        :type="selected === 0 ? 'error' : 'default'"
        :ghost="selected !== 0"
        :class="
          selected === 0 ? 'bg-red-500/10' : 'text-gray-500 border-gray-700'
        "
        text-color="white"
        strong="true"
        class="w-16 h-9 transition-all duration-300"
      >
        0
      </n-button>

      <n-button
        @click="handleClick(0.5)"
        :type="selected === 0.5 ? 'warning' : 'default'"
        :ghost="selected !== 0.5"
        :class="
          selected === 0.5
            ? 'bg-yellow-500/10'
            : 'text-gray-500 border-gray-700'
        "
        :text-color="selected === 0.5 ? 'black' : 'white'"
        strong="true"
        class="w-16 h-9 transition-all duration-300"
      >
        0.5
      </n-button>

      <n-button
        @click="handleClick(1)"
        :type="selected === 1 ? 'primary' : 'default'"
        :ghost="selected !== 1"
        :class="
          selected === 1 ? 'bg-[#63e2b7]/10' : 'text-gray-500 border-gray-700'
        "
        text-color="white"
        strong="true"
        class="w-16 h-9 transition-all duration-300"
      >
        1
      </n-button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { NButton } from "naive-ui";

const props = defineProps({
  heading: { type: String, required: true },
  title: { type: String, required: true },
  modelValue: { type: [Number, String], default: "Unchecked" },
  reference: { type: String, required: false },
});

const emit = defineEmits(["update:modelValue", "change"]);
const selected = ref(props.modelValue);

watch(
  () => props.modelValue,
  (newVal) => {
    selected.value = newVal;
  }
);

function handleClick(value) {
  const next = selected.value === value ? "Unchecked" : value;
  selected.value = next;
  emit("update:modelValue", next);
  emit("change", next);
}
</script>
