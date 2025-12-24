import { defineStore } from "pinia";
import { calculateEverything } from "../services/coreCaculate";
import coreMapping from "../assets/coreMapping.json";

export const useAssessmentStore = defineStore("assessment", {
  state: () => ({
    // 1. Cấu hình ban đầu từ Input.vue
    config: {
      targetApp: "",
      auditorName: "",
      level: 1,
      weights: {
        structure: 60,
        environment: 30,
        process: 10,
      },
    },
    // 2. Điểm số từng câu từ Main.vue
    results: {},
    // 3. Kết quả sau khi tính toán để Result.vue dùng
    finalReport: null,
    isLoading: false,
  }),

  actions: {
    // Lưu thông tin từ trang Input
    setConfig(data) {
      this.config = { ...this.config, ...data };
    },

    // Lưu điểm checklist
    saveResults(results) {
      this.results = results;
    },

    // Action "át chủ bài": Tính toán toàn bộ 5 tầng
    async generateReport() {
      this.isLoading = true;
      try {
        // Chuyển weights từ % sang decimal
        const weights = {
          "Software Structure": this.config.weights.structure / 100,
          "Software Environment": this.config.weights.environment / 100,
          "Software Process": this.config.weights.process / 100,
        };

        // Gọi hàm tính toán 5 tầng với đầy đủ 3 tham số
        const data = await calculateEverything(
          coreMapping,
          this.results,
          weights
        );
        this.finalReport = data;
        return data;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
