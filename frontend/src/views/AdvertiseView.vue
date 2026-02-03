<template>
  <div class="columns is-centered">
    <div class="column is-6">
      <h1 class="title">Advertise a New Route</h1>
      <form @submit.prevent="submitForm" class="box">
        <div class="field">
          <label class="label">Starting Location</label>
          <input type="text" class="input" v-model="form.start_location" required>
        </div>
        <div class="field">
          <label class="label">Destination</label>
          <input type="text" class="input" v-model="form.destination" required>
        </div>
        <div class="columns">
          <div class="column"><label class="label">Date</label><input type="date" class="input" v-model="form.date"
              required></div>
          <div class="column"><label class="label">Time</label><input type="time" class="input" v-model="form.time"
              required></div>
        </div>
        <div class="columns">
          <div class="column"><label class="label">Car Model</label><input type="text" class="input"
              v-model="form.car_model" required></div>
          <div class="column"><label class="label">Capacity</label><input type="number" class="input"
              v-model="form.capacity" required></div>
        </div>
        <div class="field">
          <label class="label">Description</label>
          <textarea class="textarea" v-model="form.description"></textarea>
        </div>
        <button class="button is-success is-fullwidth">Post Route</button>
      </form>
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
      form: {
        start_location: '',
        destination: '',
        date: '',
        time: '',
        car_model: '',
        capacity: 4,
        description: ''
      },
      errors: {}
    }
  },
  methods: {
    async submitForm() {
      // Validate form
      if (!this.form.start_location.trim()) {
        toast({ message: 'Starting location is required', type: 'is-warning' })
        return
      }
      if (!this.form.destination.trim()) {
        toast({ message: 'Destination is required', type: 'is-warning' })
        return
      }
      if (this.form.capacity < 1) {
        toast({ message: 'Capacity must be at least 1', type: 'is-warning' })
        return
      }

      try {
        // Convert capacity to integer
        const formData = {
          ...this.form,
          capacity: parseInt(this.form.capacity, 10)
        }
        await axios.post('/api/routes/', formData, getCSRFConfig())
        toast({ message: 'Route advertised successfully!', type: 'is-success' })
        // Small delay to ensure route is saved before redirecting
        setTimeout(() => {
          this.$router.push('/my-rides')
        }, 500)
      } catch (error) {
        const message = error.response?.data?.detail || JSON.stringify(error.response?.data) || 'Error posting route'
        console.error('Route post error:', error.response?.data)
        toast({ message, type: 'is-danger' })
      }
    }
  }
}
</script>