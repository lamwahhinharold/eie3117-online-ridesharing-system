<template>
  <div class="columns is-centered is-vcentered" style="min-height: 70vh;">
    <div class="column is-5-tablet is-4-desktop">
      <div class="box">
        <div class="has-text-centered mb-5">
          <span class="icon is-large has-text-link">
            <i class="fas fa-car-side fa-3x"></i>
          </span>
          <h1 class="title is-3 mt-3">Welcome Back</h1>
          <p class="subtitle is-6 has-text-grey">Sign in to your account</p>
        </div>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label class="label">Login ID</label>
            <div class="control has-icons-left">
              <input type="text" class="input" placeholder="Enter your username" v-model="username" required>
              <span class="icon is-left"><i class="fas fa-user"></i></span>
            </div>
          </div>
          <div class="field">
            <label class="label">Password</label>
            <div class="control has-icons-left">
              <input type="password" class="input" placeholder="Enter your password" v-model="password" required>
              <span class="icon is-left"><i class="fas fa-lock"></i></span>
            </div>
          </div>
          <div class="field mt-5">
            <button class="button is-link is-fullwidth" :class="{ 'is-loading': submitting }" :disabled="submitting">
              <span class="icon"><i class="fas fa-sign-in-alt"></i></span>
              <span>Login</span>
            </button>
          </div>
        </form>

        <hr>
        <p class="has-text-centered">
          Don't have an account?
          <RouterLink to="/register" class="has-text-link has-text-weight-semibold">Register here</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ensureCSRFToken, getCSRFConfig } from '../utils/auth'

export default {
  data() {
    return { username: '', password: '', submitting: false }
  },
  methods: {
    async submitForm() {
      this.submitting = true
      const formData = { username: this.username, password: this.password }

      try {
        await ensureCSRFToken()
        const response = await axios.post("/api/login/", formData, getCSRFConfig())

        this.$store.commit('setUser', response.data.user)
        this.$store.commit('setAuthenticated', true)
        this.$router.push('/')
      } catch (error) {
        const { toast } = await import('bulma-toast')
        toast({
          message: 'Invalid Login: ' + (error.response?.data?.detail || 'Check your credentials'),
          type: 'is-danger',
          position: 'top-center',
        })
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>