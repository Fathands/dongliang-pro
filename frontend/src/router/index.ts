import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
const workbench = () => import('../pages/workbench/index.vue')
const years = () => import('../pages/years/index.vue')
const yearsDate = () => import('../pages/years/date-detail.vue')
const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: '/workbench', },
  { path: '/workbench', name: 'workbench', component: workbench, },
  { path: '/years', name: 'years', component: years, },
  { path: '/years/date', name: 'yearsDate', component: yearsDate, },
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router