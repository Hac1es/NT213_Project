import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../pages/HomeView.vue";
import InputPage from "../pages/Input.vue";
import MainPage from "../pages/Main.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/input", name: "Input", component: InputPage },
  {
    path: "/main",
    name: "Main",
    component: MainPage,
    // Chuyển query từ URL thành prop 'config' cho component Main.vue
    props: (route) => ({
      config: {
        targetApp: route.query.targetApp,
        auditorName: route.query.auditorName,
        level: route.query.level || 1,
      },
    }),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
