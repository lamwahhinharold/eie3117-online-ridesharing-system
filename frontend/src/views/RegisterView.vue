<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="box">
        <div class="auth-header">
          <div class="auth-icon">
            <i class="fas fa-user-plus"></i>
          </div>
          <h1 class="title is-4">Create Account</h1>
          <p class="subtitle is-6">Join the ridesharing community</p>
        </div>

        <form @submit.prevent="submitForm">
          <div class="columns is-multiline">
            <div class="column is-6">
              <div class="field">
                <label class="label">Login ID (Username)</label>
                <div class="control has-icons-left">
                  <input type="text" class="input" :class="{ 'is-danger': errors.username }" placeholder="Choose a username" v-model="username" required>
                  <span class="icon is-left"><i class="fas fa-user"></i></span>
                </div>
                <p v-if="errors.username" class="help is-danger">{{ errors.username }}</p>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Nick Name</label>
                <div class="control has-icons-left">
                  <input type="text" class="input" :class="{ 'is-danger': errors.nickname }" placeholder="Your display name" v-model="nickname" required>
                  <span class="icon is-left"><i class="fas fa-id-badge"></i></span>
                </div>
                <p v-if="errors.nickname" class="help is-danger">{{ errors.nickname }}</p>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left">
              <input type="email" class="input" :class="{ 'is-danger': errors.email }" placeholder="you@example.com" v-model="email" required>
              <span class="icon is-left"><i class="fas fa-envelope"></i></span>
            </div>
            <p v-if="errors.email" class="help is-danger">{{ errors.email }}</p>
          </div>

          <div class="columns">
            <div class="column is-6">
              <div class="field">
                <label class="label">Password</label>
                <div class="control has-icons-left">
                  <input type="password" class="input" :class="{ 'is-danger': errors.password }" placeholder="Min. 8 characters" v-model="password" required>
                  <span class="icon is-left"><i class="fas fa-lock"></i></span>
                </div>
                <p v-if="errors.password" class="help is-danger">{{ errors.password }}</p>
              </div>
            </div>
            <div class="column is-6">
              <div class="field">
                <label class="label">Confirm Password</label>
                <div class="control has-icons-left">
                  <input type="password" class="input" placeholder="Re-enter password" v-model="password2" required>
                  <span class="icon is-left"><i class="fas fa-lock"></i></span>
                </div>
                <p v-if="password2 && password !== password2" class="help is-danger">Passwords do not match</p>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">User Type</label>
            <div class="control has-icons-left">
              <div class="select is-fullwidth">
                <select v-model="is_driver">
                  <option :value="false">🚶 Rider</option>
                  <option :value="true">🚗 Driver</option>
                </select>
              </div>
              <span class="icon is-left"><i class="fas fa-users"></i></span>
            </div>
          </div>

          <div class="field">
            <label class="label">Profile Image <span class="has-text-grey has-text-weight-normal">(Optional)</span></label>
            <div class="file has-name is-fullwidth is-link is-light">
              <label class="file-label">
                <input class="file-input" type="file" accept="image/*" @change="onFileChange">
                <span class="file-cta">
                  <span class="file-icon"><i class="fas fa-cloud-upload-alt"></i></span>
                  <span class="file-label">Choose image…</span>
                </span>
                <span class="file-name">{{ profile_image ? profile_image.name : 'No file chosen' }}</span>
              </label>
            </div>
            <p v-if="errors.profile_image" class="help is-danger">{{ errors.profile_image }}</p>
          </div>

          <div class="field mt-5">
            <button class="button is-link is-fullwidth" :class="{ 'is-loading': submitting }" :disabled="submitting || (password2 && password !== password2)">
              <span class="icon"><i class="fas fa-user-plus"></i></span>
              <span>Create Account</span>
            </button>
          </div>
        </form>

        <hr>
        <p class="has-text-centered" style="font-size: 0.9rem;">
          Already have an account?
          <RouterLink to="/login" class="has-text-link has-text-weight-semibold">Sign in</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'


export default {
  data() {
    return {
      username: '',
      nickname: '',
      email: '',
      password: '',
      password2: '',
      is_driver: false,
      profile_image: null,
      submitting: false,
      errors: {},
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          toast({ message: 'Image must be less than 5MB', type: 'is-warning', position: 'top-center' })
          event.target.value = ''
          this.profile_image = null
          return
        }
        this.profile_image = file
      }
    },
    async submitForm() {
      if (this.password !== this.password2) {
        toast({ message: 'Passwords do not match', type: 'is-danger', position: 'top-center' })
        return
      }

      this.errors = {}
      this.submitting = true
      const formData = new FormData()
      formData.append('username', this.username)
      formData.append('nickname', this.nickname)
      formData.append('email', this.email)
      formData.append('password', this.password)
      formData.append('is_driver', this.is_driver)

      if (this.profile_image) {
        formData.append('profile_image', this.profile_image)
      }

      try {
        await axios.post('/api/register/', formData)
        toast({ message: 'Account created! Please login.', type: 'is-success', position: 'top-center' })
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration error:', error)
        const data = error.response?.data || {}
        // Map server field errors to inline messages
        const fieldErrors = {}
        for (const field of ['username', 'nickname', 'email', 'password', 'is_driver', 'profile_image']) {
          if (data[field]) {
            fieldErrors[field] = Array.isArray(data[field]) ? data[field][0] : data[field]
          }
        }
        this.errors = fieldErrors

        const errorMsg = data.detail ||
          (Object.keys(fieldErrors).length > 0
            ? 'Please fix the highlighted errors below.'
            : 'Something went wrong')
        toast({ message: errorMsg, type: 'is-danger', position: 'top-center' })
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
  max-width: 540px;
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