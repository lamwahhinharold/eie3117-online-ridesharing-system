<template>
  <div class="columns is-centered">
    <div class="column is-4">
      <h1 class="title">Register</h1>
      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="label">Login ID (Username)</label>
          <div class="control"><input type="text" class="input" v-model="username" required></div>
        </div>
        <div class="field">
          <label class="label">Nick Name</label>
          <div class="control"><input type="text" class="input" v-model="nickname" required></div>
        </div>
        <div class="field">
          <label class="label">Email</label>
          <div class="control"><input type="email" class="input" v-model="email" required></div>
        </div>
        <div class="field">
          <label class="label">Password</label>
          <div class="control"><input type="password" class="input" v-model="password" required></div>
        </div>
        <div class="field">
          <label class="label">User Type</label>
          <div class="control">
            <div class="select">
              <select v-model="is_driver">
                <option :value="false">Rider</option>
                <option :value="true">Driver</option>
              </select>
            </div>
          </div>
        </div>
        <div class="field">
          <label class="label">Profile Image (Optional)</label>
          <div class="file has-name is-fullwidth">
            <label class="file-label">
              <input class="file-input" type="file" accept="image/*" @change="onFileChange">
              <span class="file-cta">
                <span class="file-icon">
                  <i class="fas fa-upload"></i>
                </span>
                <span class="file-label">Choose a file…</span>
              </span>
              <span class="file-name">{{ profile_image ? profile_image.name : 'No file chosen' }}</span>
            </label>
          </div>
        </div>
        <div class="field">
          <button class="button is-dark is-fullwidth">Register</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { ensureCSRFToken, getCSRFConfig } from '../utils/auth'

export default {
  data() {
    return {
      username: '',
      nickname: '',
      email: '',
      password: '',
      is_driver: false,
      profile_image: null
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
          toast({ message: 'Image must be less than 5MB', type: 'is-warning' })
          event.target.value = ''
          this.profile_image = null
          return
        }
        this.profile_image = file
      }
    },
    async submitForm() {
      // Use FormData for file upload
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
        // First, fetch the CSRF token from public endpoint
        await ensureCSRFToken()

        // For FormData, don't set Content-Type header - let browser set it automatically
        // Also import getCookie from utils
        const { getCookie } = await import('../utils/auth')
        const config = {
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
            // Don't set Content-Type, let axios handle it for FormData
          }
        }

        await axios.post('/auth/users/', formData, config)
        toast({ message: 'Account created! Please login.', type: 'is-success' })
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration error:', error)
        const errorMsg = error.response?.data?.username?.[0] ||
                        error.response?.data?.email?.[0] ||
                        error.response?.data?.profile_image?.[0] ||
                        error.response?.data?.detail ||
                        'Something went wrong'
        toast({ message: errorMsg, type: 'is-danger' })
      }
    }
  }
}
</script>