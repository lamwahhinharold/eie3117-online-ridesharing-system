import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requireLogin: true }
  },
  {
    path: '/advertise',
    name: 'advertise',
    component: () => import('../views/AdvertiseView.vue'),
    meta: { requireLogin: true }
  },
  {
    path: '/my-rides',
    name: 'my-rides',
    component: () => import('../views/MyRidesView.vue'),
    meta: { requireLogin: true }
  },
  {
    path: '/route/:id',
    name: 'RouteDetail',
    component: () => import('../views/RouteDetailView.vue'),
    props: true
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard: Check if user is logged in before entering certain pages
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router