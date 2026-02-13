<template>
  <div id="wrapper">
    <nav class="navbar is-link is-fixed-top has-shadow" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <router-link to="/" class="navbar-item">
            <i class="fas fa-car-side mr-2"></i>
            <strong>RideShare</strong>
          </router-link>
          <a
            role="button"
            class="navbar-burger"
            :class="{ 'is-active': showMobileMenu }"
            aria-label="menu"
            aria-expanded="false"
            @click="showMobileMenu = !showMobileMenu"
          >
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div class="navbar-menu" :class="{ 'is-active': showMobileMenu }">
          <div class="navbar-start">
            <router-link to="/" class="navbar-item">
              <i class="fas fa-road mr-2"></i> Browse Routes
            </router-link>
          </div>

          <div class="navbar-end">
            <template v-if="$store.state.isAuthenticated">
              <router-link to="/profile" class="navbar-item">
                <i class="fas fa-user-circle mr-2"></i>
                {{ $store.state.user.nickname || 'Profile' }}
              </router-link>
              <template v-if="$store.state.user.is_driver">
                <router-link to="/advertise" class="navbar-item">
                  <i class="fas fa-plus-circle mr-2"></i> New Route
                </router-link>
                <router-link to="/my-rides" class="navbar-item">
                  <i class="fas fa-steering-wheel mr-2"></i> My Routes
                </router-link>
              </template>
              <router-link v-else to="/my-rides" class="navbar-item">
                <i class="fas fa-ticket mr-2"></i> My Rides
              </router-link>
              <div class="navbar-item">
                <button @click="logout" class="button is-light is-small">
                  <i class="fas fa-sign-out-alt mr-1"></i> Logout
                </button>
              </div>
            </template>

            <template v-else>
              <router-link to="/login" class="navbar-item">
                <i class="fas fa-sign-in-alt mr-2"></i> Login
              </router-link>
              <div class="navbar-item">
                <router-link to="/register" class="button is-white is-outlined is-small">
                  <i class="fas fa-user-plus mr-1"></i> Register
                </router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="section mt-6 pt-5" style="min-height: calc(100vh - 160px);">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </router-view>
    </main>

    <footer class="footer has-background-dark has-text-light py-4">
      <div class="container has-text-centered">
        <p><strong class="has-text-light">EIE3117 Group 4</strong> - Online Ridesharing System</p>
        <p class="is-size-7 has-text-grey-light mt-1">The Hong Kong Polytechnic University &middot; {{ new Date().getFullYear() }}</p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from './utils/auth'

export default {
  data() {
    return {
      showMobileMenu: false,
    }
  },
  watch: {
    $route() {
      this.showMobileMenu = false
    },
  },
  created() {
    this.$store.dispatch('checkAuth')
  },
  methods: {
    async logout() {
      try {
        await axios.post('/api/logout/', {}, getCSRFConfig())
        toast({ message: 'Logged out successfully', type: 'is-success', position: 'top-center' })
        this.$store.commit('clearAuth')
        this.$router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
        toast({ message: 'Logout failed', type: 'is-danger', position: 'top-center' })
      }
    },
  },
}
</script>

<style lang="scss">
@import 'bulma/css/versions/bulma-no-dark-mode.css';

/* ── Custom brand color override (rgb(172,53,75)) ── */
:root {
  --brand: rgb(172, 53, 75);
  --brand-light: rgba(172, 53, 75, 0.1);
  --brand-dark: rgb(140, 40, 60);
  --brand-invert: #fff;
}

/* Override Bulma's is-link / has-text-link */
.navbar.is-link,
.hero.is-link {
  background-color: var(--brand) !important;
}
.navbar.is-link .navbar-item,
.navbar.is-link .navbar-link,
.navbar.is-link .navbar-burger,
.hero.is-link .title,
.hero.is-link .subtitle {
  color: var(--brand-invert) !important;
}
.navbar.is-link .navbar-item:hover,
.navbar.is-link .navbar-item:focus {
  background-color: var(--brand-dark) !important;
}
.navbar.is-link .navbar-burger:hover {
  background-color: var(--brand-dark) !important;
}
.button.is-link {
  background-color: var(--brand) !important;
  border-color: transparent !important;
  color: var(--brand-invert) !important;
}
.button.is-link:hover,
.button.is-link:focus {
  background-color: var(--brand-dark) !important;
}
.button.is-link.is-loading::after {
  border-color: transparent transparent var(--brand-invert) var(--brand-invert) !important;
}
.has-text-link {
  color: var(--brand) !important;
}
a.has-text-link:hover {
  color: var(--brand-dark) !important;
}
.tag.is-link.is-light,
.file.is-link.is-light .file-cta {
  background-color: var(--brand-light) !important;
  color: var(--brand) !important;
}
.tag.is-info.is-light {
  background-color: var(--brand-light) !important;
  color: var(--brand) !important;
}
.has-text-info {
  color: var(--brand) !important;
}
.pagination-link.is-current {
  background-color: var(--brand) !important;
  border-color: var(--brand) !important;
  color: var(--brand-invert) !important;
}
.progress.is-success::-webkit-progress-value { background-color: #48c78e; }
.progress.is-warning::-webkit-progress-value { background-color: #ffe08a; }
.progress.is-danger::-webkit-progress-value { background-color: #f14668; }

/* ── Sticky footer via flexbox ── */
#wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
#wrapper > main {
  flex: 1;
}

/* Page transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Card polish */
.card {
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,.12);
  transform: translateY(-2px);
}

/* Fix disabled pagination links */
.pagination-previous[disabled],
.pagination-next[disabled] {
  pointer-events: none;
  opacity: 0.5;
}
</style>
