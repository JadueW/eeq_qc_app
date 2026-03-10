import { createRouter, createWebHistory } from 'vue-router'
import ProjectListView from '../views/ProjectListView.vue'
import ProjectDetailView from '../views/ProjectDetailView.vue'
import FileDetailView from '../views/FileDetailView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ProjectListView },
    { path: '/projects/:id', component: ProjectDetailView },
    { path: '/files/:id', component: FileDetailView },
  ],
})

export default router