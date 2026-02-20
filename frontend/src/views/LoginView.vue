<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="box">
        <div class="auth-header">
          <div class="auth-icon">
            <i class="fas fa-car-side"></i>
          </div>
          <h1 class="title is-4">Welcome Back</h1>
          <p class="subtitle is-6">Sign in to continue to RideShare</p>
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
        <p class="has-text-centered" style="font-size: 0.9rem;">
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

<style scoped>
.auth-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 2rem 1rem;
}
.auth-card {
  width: 100%;
  max-width: 420px;
}
.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}
.auth-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: var(--primary);
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}
.auth-header .title {
  margin-bottom: 0.25rem;
}
</style>