<template>
  <div class="container">
    <div class="columns is-centered">
      <div class="column is-6">
        <div class="box">
          <h1 class="title">My Profile</h1>
          <hr>

          <!-- Profile Image -->
          <div class="field has-text-centered mb-5">
            <figure class="image is-128x128 is-inline-block">
              <img v-if="getProfileImageUrl()" :src="getProfileImageUrl()" :alt="user.username" class="is-rounded">
              <img v-else src="https://via.placeholder.com/128" :alt="user.username" class="is-rounded">
            </figure>
          </div>

          <!-- Display Mode -->
          <div v-if="!isEditing" class="content">
            <div class="field">
              <label class="label">Username</label>
              <div class="control">
                <input type="text" class="input" :value="user.username" disabled>
              </div>
            </div>

            <div class="field">
              <label class="label">Nickname</label>
              <div class="control">
                <input type="text" class="input" :value="user.nickname" disabled>
              </div>
            </div>

            <div class="field">
              <label class="label">Email</label>
              <div class="control">
                <input type="email" class="input" :value="user.email" disabled>
              </div>
            </div>

            <div class="field">
              <label class="label">User Type</label>
              <div class="control">
                <input type="text" class="input" :value="user.is_driver ? 'Driver' : 'Rider'" disabled>
              </div>
            </div>

            <div class="field is-grouped">
              <div class="control">
                <button @click="isEditing = true" class="button is-info">Edit Profile</button>
              </div>
              <div class="control">
                <router-link to="/" class="button is-light">Back</router-link>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <div v-else>
            <form @submit.prevent="submitEdit">
              <div class="field">
                <label class="label">Nickname</label>
                <div class="control">
                  <input type="text" class="input" v-model="editForm.nickname" required>
                </div>
              </div>

              <div class="field">
                <label class="label">Email</label>
                <div class="control">
                  <input type="email" class="input" v-model="editForm.email" required>
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
                    <span class="file-name">{{ editForm.profile_image ? editForm.profile_image.name : 'No file chosen' }}</span>
                  </label>
                </div>
              </div>

              <div class="field is-grouped">
                <div class="control">
                  <button type="submit" class="button is-success">Save Changes</button>
                </div>
                <div class="control">
                  <button type="button" @click="cancelEdit" class="button is-light">Cancel</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from '../utils/auth'

export default {
  data() {
    return {
      isEditing: false,
      user: {
        username: '',
        nickname: '',
        email: '',
        is_driver: false,
        profile_image: null
      },
      editForm: {
        nickname: '',
        email: '',
        profile_image: null
      }
    }
  },
  mounted() {
    this.fetchUserProfile()
  },
  methods: {
    getProfileImageUrl() {
      if (this.user.profile_image) {
        // Construct full URL for image display
        // Backend returns relative path like "/media/profiles/image_XXX.jpg"
        const baseURL = axios.defaults.baseURL || 'http://localhost:8000'
        return `${baseURL}${this.user.profile_image}`
      }
      return null
    },
    async fetchUserProfile() {
      try {
        const response = await axios.get('/api/user/')
        this.user = response.data
        this.editForm.nickname = this.user.nickname
        this.editForm.email = this.user.email
      } catch (error) {
        console.error('Error fetching profile:', error)
        toast({ message: 'Failed to load profile', type: 'is-danger' })
      }
    },
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
          toast({ message: 'Image must be less than 5MB', type: 'is-warning' })
          event.target.value = ''
          this.editForm.profile_image = null
          return
        }
        this.editForm.profile_image = file
      }
    },
    async submitEdit() {
      try {
        const formData = new FormData()
        formData.append('nickname', this.editForm.nickname)
        formData.append('email', this.editForm.email)

        if (this.editForm.profile_image) {
          formData.append('profile_image', this.editForm.profile_image)
        }

        await axios.patch('/api/user/', formData, {
          ...getCSRFConfig(),
          headers: {
            ...getCSRFConfig().headers,
            'Content-Type': 'multipart/form-data'
          }
        })

        // Update store with new user data
        const response = await axios.get('/api/user/')
        this.$store.commit('setUser', response.data)

        toast({ message: 'Profile updated successfully!', type: 'is-success' })
        this.isEditing = false
      } catch (error) {
        console.error('Error updating profile:', error)
        const errorMsg = error.response?.data?.detail || 'Failed to update profile'
        toast({ message: errorMsg, type: 'is-danger' })
      }
    },
    cancelEdit() {
      this.editForm.nickname = this.user.nickname
      this.editForm.email = this.user.email
      this.editForm.profile_image = null
      this.isEditing = false
    }
  }
}
</script>
