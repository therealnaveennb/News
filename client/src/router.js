// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import DashBoard from './components/DashBoard.vue';
import ArticleDetail from './components/ArticleDetail.vue';
import AboutPage from './components/AboutPage.vue';
const routes = [
  { path: '/', name: 'Dashboard', component: DashBoard },
  { path: '/articles', name: 'Dashboard', component: DashBoard },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: ArticleDetail, // Import the ArticleDetail component
  },
  { path: '/about', name: 'AboutPage', component:AboutPage}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
