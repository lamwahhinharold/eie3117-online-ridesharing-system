<template>
  <div>
    <section class="page-hero">
      <div class="container">
        <h1 class="title"><i class="fas fa-id-card mr-2"></i> My Profile</h1>
        <p class="subtitle">Manage your account details</p>
      </div>
    </section>

    <div class="container">
      <div class="columns is-centered">
        <div class="column is-6">
          <div class="box">
            <!-- Avatar -->
            <div class="profile-avatar-section">
              <figure class="image is-128x128" style="margin: 0 auto;">
                <img v-if="getProfileImageUrl()" :src="getProfileImageUrl()" :alt="user.username" class="is-rounded profile-avatar">
                <img v-else src="https://via.placeholder.com/128?text=%F0%9F%91%A4" :alt="user.username" class="is-rounded profile-avatar">
              </figure>
              <p class="profile-name">{{ user.nickname || user.username }}</p>
              <span class="tag is-medium" :class="user.is_driver ? 'is-info' : 'is-success'">
                <i class="fas mr-1" :class="user.is_driver ? 'fa-car' : 'fa-walking'"></i>
                {{ user.is_driver ? 'Driver' : 'Rider' }}
              </span>
            </div>

            <hr>

            <!-- Display Mode -->
            <div v-if="!isEditing">
              <div class="profile-field">
                <div class="profile-field-icon"><i class="fas fa-user"></i></div>
                <div>
                  <p class="profile-field-label">Username</p>
                  <p class="profile-field-value">{{ user.username }}</p>
                </div>
              </div>
              <div class="profile-field">
                <div class="profile-field-icon"><i class="fas fa-id-badge"></i></div>
                <div>
                  <p class="profile-field-label">Nickname</p>
                  <p class="profile-field-value">{{ user.nickname || '-' }}</p>
                </div>
              </div>
              <div class="profile-field">
                <div class="profile-field-icon"><i class="fas fa-envelope"></i></div>
                <div>
                  <p class="profile-field-label">Email</p>
                  <p class="profile-field-value">{{ user.email }}</p>
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

        await axios.patch('/api/user/', formData, getCSRFConfig())

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

<style scoped>
.profile-avatar-section {
  text-align: center;
  margin-bottom: 2rem;
}
.profile-avatar {
  object-fit: cover;
  width: 128px;
  height: 128px;
  border: 3px solid var(--border);
}
.profile-name {
  font-size: 1.15rem;
  font-weight: 700;
  margin-top: 0.75rem;
  margin-bottom: 0.5rem;
}
.profile-field {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
.profile-field-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}
.profile-field-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-bottom: 0.1rem;
}
.profile-field-value {
  font-weight: 600;
  font-size: 0.95rem;
}
</style>
