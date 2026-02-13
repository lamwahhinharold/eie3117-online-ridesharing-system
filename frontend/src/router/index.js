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
    meta: { requireLogin: true, requireDriver: true }
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
  {
    path: '/edit-route/:id',
    name: 'EditRoute',
    component: () => import('../views/EditRouteView.vue'),
    meta: { requireLogin: true, requireDriver: true }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation Guard: Wait for auth check then verify login/role
router.beforeEach(async (to, from, next) => {
  // Wait for the initial session check to complete before guarding
  await store.authReady

  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else if (to.matched.some(record => record.meta.requireDriver) && !store.state.user.is_driver) {
    next('/')
  } else {
    next()
  }
})

export default router