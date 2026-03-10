import { createRouter, createWebHistory } from 'vue-router'
import ProjectListView from '../views/ProjectListView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: ProjectListView }],
})

export default router
