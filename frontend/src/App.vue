<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link
          to="/"
          class="navbar-item has-background-primary-00 has-text-primary-00-invert"
          style="text-decoration: underline"
          ><strong>RideShare</strong></router-link
        >
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <router-link to="/" class="navbar-item">Available Routes</router-link>
        </div>

        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            <router-link to="/profile" class="navbar-item">{{
              $store.state.user.nickname || 'Profile'
            }}</router-link>
            <template v-if="$store.state.user.is_driver">
              <router-link to="/advertise" class="navbar-item">Advertise Route</router-link>
              <router-link to="/my-rides" class="navbar-item">My Routes</router-link>
            </template>
            <router-link v-else to="/my-rides" class="navbar-item">My Rides</router-link>
            <button @click="logout" class="navbar-item is-danger button has-text-primary-15-invert">
              Logout
            </button>
          </template>

          <template v-else>
            <router-link to="/login" class="navbar-item">Login</router-link>
            <router-link to="/register" class="navbar-item">Register</router-link>
          </template>
        </div>
      </div>
    </nav>

    <section class="section">
      <router-view />
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { ensureCSRFToken, getCSRFConfig } from './utils/auth'

export default {
  async beforeCreate() {
    this.$store.commit('initializeStore')

    // Check if user is logged in via session cookie
    try {
      await ensureCSRFToken()
      const userRes = await axios.get('/api/user/')
      this.$store.commit('setUser', userRes.data)
    } catch (error) {
      // Not logged in, clear auth state
      this.$store.commit('clearAuth')
    }
  },
  methods: {
    async logout() {
      try {
        await axios.post('/api/logout/', {}, getCSRFConfig())
        toast({ message: 'Log out successfully', type: 'is-success' })
        this.$store.commit('clearAuth')
        this.$router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
        toast({ message: 'Log out failed', type: 'is-danger' })
      }
    },
  },
}
</script>

<style lang="scss">
@import 'bulma/css/versions/bulma-no-dark-mode.css';
</style>
