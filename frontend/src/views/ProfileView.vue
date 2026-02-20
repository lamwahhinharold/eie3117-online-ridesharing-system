<template>
  <div>
    <section class="hero is-link is-small mb-5">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-3"><i class="fas fa-id-card mr-2"></i> My Profile</h1>
          <p class="subtitle is-6">Manage your account details</p>
        </div>
      </div>
    </section>

    <div class="container">
      <div class="columns is-centered">
        <div class="column is-6">
          <div class="box">
            <!-- Avatar -->
            <div class="has-text-centered mb-5">
              <figure class="image is-128x128 is-inline-block">
                <img v-if="getProfileImageUrl()" :src="getProfileImageUrl()" :alt="user.username" class="is-rounded" style="object-fit: cover; width: 128px; height: 128px;">
                <img v-else src="https://via.placeholder.com/128?text=👤" :alt="user.username" class="is-rounded">
              </figure>
              <p class="is-size-5 has-text-weight-semibold mt-3">{{ user.nickname || user.username }}</p>
              <span class="tag is-medium mt-1" :class="user.is_driver ? 'is-link is-light' : 'is-success is-light'">
                <i class="fas mr-1" :class="user.is_driver ? 'fa-car' : 'fa-walking'"></i>
                {{ user.is_driver ? 'Driver' : 'Rider' }}
              </span>
            </div>

            <hr>

            <!-- Display Mode -->
            <div v-if="!isEditing">
              <div class="is-flex is-align-items-center mb-4">
                <span class="icon has-text-link mr-3"><i class="fas fa-user"></i></span>
                <div>
                  <p class="is-size-7 has-text-grey">Username</p>
                  <p class="has-text-weight-semibold">{{ user.username }}</p>
                </div>
              </div>
              <div class="is-flex is-align-items-center mb-4">
                <span class="icon has-text-link mr-3"><i class="fas fa-id-badge"></i></span>
                <div>
                  <p class="is-size-7 has-text-grey">Nickname</p>
                  <p class="has-text-weight-semibold">{{ user.nickname || '-' }}</p>
                </div>
              </div>
              <div class="is-flex is-align-items-center mb-4">
                <span class="icon has-text-link mr-3"><i class="fas fa-envelope"></i></span>
                <div>
                  <p class="is-size-7 has-text-grey">Email</p>
                  <p class="has-text-weight-semibold">{{ user.email }}</p>
                </div>
              </div>

              <div class="buttons mt-5">
                <button @click="isEditing = true" class="button is-link">
                  <span class="icon"><i class="fas fa-pen"></i></span>
                  <span>Edit Profile</span>
                </button>
                <router-link to="/" class="button is-light">
                  <span class="icon"><i class="fas fa-arrow-left"></i></span>
                  <span>Back</span>
                </router-link>
              </div>
            </div>

            <!-- Edit Mode -->
            <div v-else>
              <form @submit.prevent="submitEdit">
                <div class="field">
                  <label class="label">Nickname</label>
                  <div class="control has-icons-left">
                    <input type="text" class="input" v-model="editForm.nickname" required>
                    <span class="icon is-left"><i class="fas fa-id-badge"></i></span>
                  </div>
                </div>
                <div class="field">
                  <label class="label">Email</label>
                  <div class="control has-icons-left">
                    <input type="email" class="input" v-model="editForm.email" required>
                    <span class="icon is-left"><i class="fas fa-envelope"></i></span>
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
                      <span class="file-name">{{ editForm.profile_image ? editForm.profile_image.name : 'No file chosen' }}</span>
                    </label>
                  </div>
                </div>
                <div class="buttons mt-5">
                  <button type="submit" class="button is-success" :class="{ 'is-loading': submitting }" :disabled="submitting">
                    <span class="icon"><i class="fas fa-check"></i></span>
                    <span>Save Changes</span>
                  </button>
                  <button type="button" @click="cancelEdit" class="button is-light">
                    <span class="icon"><i class="fas fa-times"></i></span>
                    <span>Cancel</span>
                  </button>
                </div>
              </form>
            </div>
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
      submitting: false,
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
        toast({ message: 'Failed to load profile', type: 'is-danger', position: 'top-center' })
      }
    },
    onFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          toast({ message: 'Image must be less than 5MB', type: 'is-warning', position: 'top-center' })
          event.target.value = ''
          this.editForm.profile_image = null
          return
        }
        this.editForm.profile_image = file
      }
    },
    async submitEdit() {
      this.submitting = true
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

        const response = await axios.get('/api/user/')
        this.$store.commit('setUser', response.data)

        toast({ message: 'Profile updated successfully!', type: 'is-success', position: 'top-center' })
        this.isEditing = false
      } catch (error) {
        console.error('Error updating profile:', error)
        const errorMsg = error.response?.data?.detail || 'Failed to update profile'
        toast({ message: errorMsg, type: 'is-danger', position: 'top-center' })
      } finally {
        this.submitting = false
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
