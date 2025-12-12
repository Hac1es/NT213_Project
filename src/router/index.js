import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "../pages/LandingPage.vue";
import MainPage from "../pages/Main.vue";
import HomeView from "../pages/HomeView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/", name: "Landing", component: LandingPage },
  { path: "/main", name: "Main", component: MainPage },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
