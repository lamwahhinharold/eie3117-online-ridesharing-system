<template>
  <div>
    <section class="hero is-link is-small mb-5">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-3"><i class="fas fa-bullhorn mr-2"></i> Advertise a Route</h1>
          <p class="subtitle is-6">Share your ride with others</p>
        </div>
      </div>
    </section>

    <div class="container">
      <div class="columns is-centered">
        <div class="column is-7">
          <RouteForm @submit="handleCreate" :loading="submitting" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from '../utils/auth'
import RouteForm from '../components/RouteForm.vue'

export default {
  components: { RouteForm },
  data() {
    return {
      submitting: false,
    }
  },
  methods: {
    async handleCreate(formData) {
      this.submitting = true
      try {
        await axios.post('/api/routes/', formData, getCSRFConfig())
        toast({ message: 'Route advertised successfully!', type: 'is-success', position: 'top-center' })
        this.$router.push('/my-rides')
      } catch (error) {
        const message = error.response?.data?.detail || JSON.stringify(error.response?.data) || 'Error posting route'
        console.error('Route post error:', error.response?.data)
        toast({ message, type: 'is-danger', position: 'top-center' })
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>