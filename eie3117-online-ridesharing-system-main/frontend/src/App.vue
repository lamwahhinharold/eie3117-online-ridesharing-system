<template>
  <div id="wrapper">
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <router-link to="/" class="navbar-item brand-logo">
            <span class="brand-icon-wrap">
              <i class="fas fa-car-side"></i>
            </span>
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
              <i class="fas fa-compass mr-2"></i> Browse Routes
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
                  <i class="fas fa-route mr-2"></i> My Routes
                </router-link>
              </template>
              <router-link v-else to="/my-rides" class="navbar-item">
                <i class="fas fa-ticket mr-2"></i> My Rides
              </router-link>
              <div class="navbar-item">
                <button @click="logout" class="button is-small is-outlined nav-logout-btn">
                  <span class="icon is-small"><i class="fas fa-sign-out-alt"></i></span>
                  <span>Logout</span>
                </button>
              </div>
            </template>

            <template v-else>
              <router-link to="/login" class="navbar-item">
                <i class="fas fa-sign-in-alt mr-2"></i> Login
              </router-link>
              <div class="navbar-item">
                <router-link to="/register" class="button is-primary is-small nav-register-btn">
                  <span class="icon is-small"><i class="fas fa-user-plus"></i></span>
                  <span>Register</span>
                </router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </router-view>
    </main>

    <footer class="footer site-footer">
      <div class="container has-text-centered">
        <p class="footer-brand"><strong>RideShare</strong> - EIE3117 Group 4</p>
        <p class="footer-sub">The Hong Kong Polytechnic University &copy; {{ new Date().getFullYear() }}</p>
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

/* ═══════════════════════════════════════════════════════
   ENTERPRISE DESIGN SYSTEM   ═══════════════════════════════════════════════════════ */

:root {
  /* ── Brand palette (Slate Navy) ── */
  --primary:       #2c3e6b;
  --primary-dark:  #1e2d4f;
  --primary-light: rgba(44, 62, 107, 0.07);
  --primary-invert:#ffffff;

  /* ── Surfaces ── */
  --bg:            #f5f7fa;
  --surface:       #ffffff;
  --border:        #e8ecf1;

  /* ── Text ── */
  --text-primary:  #1a1a2e;
  --text-secondary:#7a7a7a;
  --text-muted:    #a0a4ab;

  /* ── Semantic ── */
  --success:       #3ecf8e;
  --warning:       #f5a623;
  --danger:        #e74c5f;
  --info:          #4a9eff;

  /* ── Elevation ── */
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.04);
  --shadow:     0 4px 12px rgba(0,0,0,0.05);
  --shadow-md:  0 8px 24px rgba(0,0,0,0.08);
  --shadow-lg:  0 12px 36px rgba(0,0,0,0.10);

  /* ── Shape ── */
  --radius:     6px;
  --radius-lg:  10px;

  /* ── Motion ── */
  --ease:       0.2s ease;
}

/* ── Base ── */
html {
  background-color: var(--bg);
}
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── Typography ── */
.title, .subtitle {
  font-family: inherit;
  letter-spacing: -0.01em;
}
.title {
  color: var(--text-primary);
  font-weight: 700;
}
.subtitle {
  color: var(--text-secondary);
}

/* ═══════════════════ NAVBAR ═══════════════════ */
.navbar {
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  border-bottom: 1px solid var(--border);
  min-height: 3.5rem;
}
.navbar .container { max-width: 1140px; }
.navbar-item, .navbar-link {
  color: var(--text-primary);
  font-size: 0.9rem;
  font-weight: 500;
  transition: color var(--ease), background var(--ease);
  border-radius: var(--radius);
}
.navbar-item:hover, .navbar-item:focus,
.navbar-link:hover, .navbar-link:focus {
  background: var(--primary-light);
  color: var(--primary);
}
.navbar-item.router-link-active:not(.brand-logo) {
  color: var(--primary);
  background: var(--primary-light);
}
.brand-logo {
  font-size: 1.05rem;
  gap: 0.45rem;
  display: flex;
  align-items: center;
  color: var(--primary) !important;
}
.brand-logo:hover { background: transparent !important; }
.brand-icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: var(--radius);
  background: var(--primary);
  color: #fff;
  font-size: 0.8rem;
}
.nav-logout-btn {
  border-color: var(--border) !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius) !important;
  font-weight: 500 !important;
  transition: all var(--ease) !important;
}
.nav-logout-btn:hover {
  border-color: var(--danger) !important;
  color: var(--danger) !important;
  background: rgba(231, 76, 95, 0.06) !important;
}
.nav-register-btn {
  background: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
  border-radius: var(--radius) !important;
  font-weight: 600 !important;
  transition: all var(--ease) !important;
}
.nav-register-btn:hover {
  background: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(44, 62, 107, 0.25);
}
.navbar-burger {
  color: var(--text-primary);
}
.navbar-burger:hover {
  background: var(--primary-light);
  color: var(--primary);
}

/* ═══════════════════ LAYOUT ═══════════════════ */
#wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--bg);
}
.main-content {
  flex: 1;
  padding-top: calc(3.5rem + 2rem);
  padding-bottom: 3rem;
}

/* ═══════════════════ FOOTER ═══════════════════ */
.site-footer {
  background: var(--text-primary) !important;
  padding: 1.5rem 1rem !important;
}
.footer-brand {
  color: #fff;
  font-size: 0.9rem;
}
.footer-brand strong { color: #fff; }
.footer-sub {
  color: rgba(255,255,255,0.45);
  font-size: 0.78rem;
  margin-top: 0.25rem;
}

/* ═══════════════════ CARDS ═══════════════════ */
.card {
  background: var(--surface);
  border-radius: var(--radius-lg) !important;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  transition: box-shadow var(--ease), transform var(--ease);
  overflow: hidden;
}
.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.card-footer {
  border-top: 1px solid var(--border) !important;
}
.card-footer-item {
  font-weight: 500;
  font-size: 0.88rem;
  transition: background var(--ease), color var(--ease);
  color: var(--primary) !important;
}
.card-footer-item:hover {
  background: var(--primary-light);
}
.card-footer-item.has-text-danger,
.card-footer-item.has-text-danger:hover {
  color: var(--danger) !important;
}
.card-footer-item.has-text-danger:hover {
  background: rgba(231, 76, 95, 0.06);
}
.card-footer-item.has-text-info {
  color: var(--info) !important;
}
.card-footer-item.has-text-info:hover {
  background: rgba(74, 158, 255, 0.06);
}

/* ═══════════════════ BOX ═══════════════════ */
.box {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

/* ═══════════════════ BUTTONS ═══════════════════ */
.button {
  border-radius: var(--radius) !important;
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: -0.005em;
  transition: all var(--ease);
}
.button.is-link,
.button.is-primary {
  background-color: var(--primary) !important;
  border-color: transparent !important;
  color: var(--primary-invert) !important;
}
.button.is-link:hover, .button.is-link:focus,
.button.is-primary:hover, .button.is-primary:focus {
  background-color: var(--primary-dark) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(44, 62, 107, 0.3);
}
.button.is-link.is-loading::after,
.button.is-primary.is-loading::after {
  border-color: transparent transparent #fff #fff !important;
}
.button.is-light {
  background: var(--bg) !important;
  color: var(--text-primary) !important;
  border-color: var(--border) !important;
}
.button.is-light:hover {
  background: #ebeef3 !important;
}
.button.is-success {
  background-color: var(--success) !important;
  border-color: transparent !important;
}
.button.is-success:hover {
  filter: brightness(0.92);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(62, 207, 142, 0.3);
}
.button.is-danger {
  background-color: var(--danger) !important;
  border-color: transparent !important;
}
.button.is-danger:hover {
  filter: brightness(0.92);
  transform: translateY(-1px);
}

/* ═══════════════════ FORM ELEMENTS ═══════════════════ */
.input, .textarea, .select select {
  border-radius: var(--radius) !important;
  border-color: var(--border) !important;
  box-shadow: none !important;
  font-family: inherit;
  font-size: 0.92rem;
  transition: border-color var(--ease), box-shadow var(--ease);
}
.input:focus, .textarea:focus, .select select:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px var(--primary-light) !important;
}
.input::placeholder, .textarea::placeholder {
  color: var(--text-muted);
}
.label {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.88rem;
  letter-spacing: -0.005em;
}

/* ═══════════════════ TAGS ═══════════════════ */
.tag {
  border-radius: var(--radius) !important;
  font-weight: 600;
  font-size: 0.78rem;
  letter-spacing: 0.01em;
}
.tag.is-success {
  background-color: rgba(62, 207, 142, 0.12) !important;
  color: #1a8a5c !important;
}
.tag.is-warning {
  background-color: rgba(245, 166, 35, 0.12) !important;
  color: #946316 !important;
}
.tag.is-danger {
  background-color: rgba(231, 76, 95, 0.10) !important;
  color: #b53a4a !important;
}
.tag.is-info,
.tag.is-info.is-light {
  background-color: var(--primary-light) !important;
  color: var(--primary) !important;
}
.tag.is-link.is-light {
  background-color: var(--primary-light) !important;
  color: var(--primary) !important;
}
.tag.is-light.is-info {
  background-color: var(--primary-light) !important;
  color: var(--primary) !important;
}

/* ═══════════════════ NOTIFICATIONS ═══════════════════ */
.notification {
  border-radius: var(--radius-lg) !important;
  border: none;
  font-size: 0.92rem;
}
.notification.is-warning.is-light {
  background: rgba(245, 166, 35, 0.08) !important;
  color: #946316 !important;
}
.notification.is-danger.is-light {
  background: rgba(231, 76, 95, 0.08) !important;
  color: #b53a4a !important;
}
.notification.is-info.is-light {
  background: var(--primary-light) !important;
  color: var(--primary) !important;
}

/* ═══════════════════ PROGRESS BARS ═══════════════════ */
.progress {
  border-radius: 20px !important;
  height: 0.5rem !important;
}
.progress::-webkit-progress-bar {
  background-color: #eef0f4;
  border-radius: 20px;
}
.progress.is-success::-webkit-progress-value {
  background: linear-gradient(90deg, #3ecf8e, #34b87d);
  border-radius: 20px;
}
.progress.is-warning::-webkit-progress-value {
  background: linear-gradient(90deg, #f5a623, #e09415);
  border-radius: 20px;
}
.progress.is-danger::-webkit-progress-value {
  background: linear-gradient(90deg, #e74c5f, #d43a4d);
  border-radius: 20px;
}

/* ═══════════════════ PAGINATION ═══════════════════ */
.pagination-link, .pagination-previous, .pagination-next {
  border-radius: var(--radius) !important;
  border-color: var(--border) !important;
  font-weight: 500;
  font-size: 0.88rem;
  transition: all var(--ease);
}
.pagination-link:hover, .pagination-previous:hover, .pagination-next:hover {
  border-color: var(--primary) !important;
  color: var(--primary) !important;
}
.pagination-link.is-current {
  background-color: var(--primary) !important;
  border-color: var(--primary) !important;
  color: #fff !important;
}
.pagination-previous[disabled],
.pagination-next[disabled] {
  pointer-events: none;
  opacity: 0.4;
}

/* ═══════════════════ HERO SECTIONS ═══════════════════ */
.page-hero {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  padding: 2.5rem 1.5rem;
  margin-bottom: 2rem;
}
.page-hero .title {
  color: #fff !important;
  font-size: 1.6rem;
  font-weight: 700;
}
.page-hero .subtitle {
  color: rgba(255,255,255,0.7) !important;
  font-size: 0.95rem;
}

/* ═══════════════════ FILE UPLOAD ═══════════════════ */
.file.is-link .file-cta,
.file.is-link.is-light .file-cta {
  background: var(--primary-light) !important;
  color: var(--primary) !important;
  border-color: var(--border) !important;
  border-radius: var(--radius) 0 0 var(--radius) !important;
}
.file-name {
  border-color: var(--border) !important;
  border-radius: 0 var(--radius) var(--radius) 0 !important;
  font-size: 0.88rem;
}

/* ═══════════════════ TEXT OVERRIDES ═══════════════════ */
.has-text-link { color: var(--primary) !important; }
a.has-text-link:hover { color: var(--primary-dark) !important; }
.has-text-info { color: var(--primary) !important; }

/* ═══════════════════ UTILITY ═══════════════════ */
.has-bg-surface { background: var(--surface); }
.has-bg-page { background: var(--bg); }

/* expired card tint */
.has-background-warning-light {
  background-color: rgba(245, 166, 35, 0.04) !important;
}

/* ═══════════════════ SELECT ═══════════════════ */
.select::after {
  border-color: var(--primary) !important;
}

/* ═══════════════════ HR ═══════════════════ */
hr {
  background-color: var(--border);
  height: 1px;
}

/* ═══════════════════ PAGE TRANSITION ═══════════════════ */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ═══════════════════ SCROLLBAR ═══════════════════ */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
  background: #ccd0d8;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: #b0b5bf; }
</style>
