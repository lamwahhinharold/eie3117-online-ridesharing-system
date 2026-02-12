<template>
  <div class="columns is-centered">
    <div class="column is-4">
      <h1 class="title">Login</h1>
      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="label">Login ID</label>
          <div class="control"><input type="text" class="input" v-model="username"></div>
        </div>
        <div class="field">
          <label class="label">Password</label>
          <div class="control"><input type="password" class="input" v-model="password"></div>
        </div>
        <div class="field">
          <button class="button is-link is-fullwidth">Login</button>
        </div>
        Don't have an account? <RouterLink to="/register">Click here</RouterLink> to register!
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ensureCSRFToken, getCSRFConfig } from '../utils/auth'

export default {
  data() {
    return { username: '', password: '' }
  },
  methods: {
    async submitForm() {
      const formData = { username: this.username, password: this.password }

      try {
        // Fetch CSRF token first from public endpoint
        await ensureCSRFToken()

        const response = await axios.post("/api/login/", formData, getCSRFConfig())

        // Session cookie is automatically set by the server
        // No need to store tokens in localStorage
        this.$store.commit('setUser', response.data.user)
        this.$store.commit('setAuthenticated', true)

        this.$router.push('/')
      } catch (error) {
        const { toast } = await import('bulma-toast')
        toast({
          message: 'Invalid Login: ' + (error.response?.data?.detail || 'Check your credentials'),
          type: 'is-danger'
        })
      }
    }
  }
}
</script>