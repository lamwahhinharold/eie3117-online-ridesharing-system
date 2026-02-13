<template>
  <div>
    <section class="hero is-link is-small mb-5">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-3"><i class="fas fa-pen-to-square mr-2"></i> Edit Route</h1>
          <p class="subtitle is-6">Update your ride details</p>
        </div>
      </div>
    </section>

    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large has-text-link"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
        <p class="mt-3 has-text-grey">Loading route...</p>
      </div>

      <div v-else class="columns is-centered">
        <div class="column is-7">
          <form @submit.prevent="submitForm" class="box">
            <!-- Route endpoints -->
            <p class="is-size-5 has-text-weight-semibold mb-3"><i class="fas fa-route has-text-link mr-2"></i> Route</p>
            <div class="field">
              <label class="label">Starting Location</label>
              <div class="control has-icons-left">
                <input type="text" class="input" v-model="form.start_location" required>
                <span class="icon is-left"><i class="fas fa-map-marker-alt"></i></span>
              </div>
            </div>
            <div class="field">
              <label class="label">Destination</label>
              <div class="control has-icons-left">
                <input type="text" class="input" v-model="form.destination" required>
                <span class="icon is-left"><i class="fas fa-flag-checkered"></i></span>
              </div>
            </div>

            <hr>

            <!-- Schedule -->
            <p class="is-size-5 has-text-weight-semibold mb-3"><i class="fas fa-calendar-alt has-text-link mr-2"></i> Schedule</p>
            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Date</label>
                  <div class="control has-icons-left">
                    <input type="date" class="input" v-model="form.date" required>
                    <span class="icon is-left"><i class="fas fa-calendar"></i></span>
                  </div>
                </div>
              </div>
              <div class="column">
                <div class="field">
                  <label class="label">Time</label>
                  <div class="control has-icons-left">
                    <input type="time" class="input" v-model="form.time" required>
                    <span class="icon is-left"><i class="fas fa-clock"></i></span>
                  </div>
                </div>
              </div>
            </div>

            <hr>

            <!-- Vehicle -->
            <p class="is-size-5 has-text-weight-semibold mb-3"><i class="fas fa-car has-text-link mr-2"></i> Vehicle</p>
            <div class="columns">
              <div class="column">
                <div class="field">
                  <label class="label">Car Model</label>
                  <div class="control has-icons-left">
                    <input type="text" class="input" v-model="form.car_model" required>
                    <span class="icon is-left"><i class="fas fa-car-side"></i></span>
                  </div>
                </div>
              </div>
              <div class="column is-4">
                <div class="field">
                  <label class="label">Capacity</label>
                  <div class="control has-icons-left">
                    <input type="number" class="input" v-model="form.capacity" min="1" max="50" required>
                    <span class="icon is-left"><i class="fas fa-users"></i></span>
                  </div>
                </div>
              </div>
            </div>

            <div class="field">
              <label class="label">Description <span class="has-text-grey has-text-weight-normal">(Optional)</span></label>
              <div class="control">
                <textarea class="textarea" placeholder="Any additional details..." v-model="form.description"></textarea>
              </div>
            </div>

            <div class="buttons mt-5">
              <button type="submit" class="button is-link is-medium is-expanded" :class="{ 'is-loading': submitting }" :disabled="submitting">
                <span class="icon"><i class="fas fa-save"></i></span>
                <span>Save Changes</span>
              </button>
              <button type="button" class="button is-light is-medium" @click="$router.push('/my-rides')">
                <span class="icon"><i class="fas fa-times"></i></span>
                <span>Cancel</span>
              </button>
            </div>
          </form>
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
      loading: true,
      submitting: false,
      form: {
        start_location: '',
        destination: '',
        date: '',
        time: '',
        car_model: '',
        capacity: 1,
        description: '',
      },
    }
  },
  async mounted() {
    const id = this.$route.params.id
    try {
      const response = await axios.get(`/api/routes/${id}/`)
      const route = response.data
      if (route.driver !== this.$store.state.user.id) {
        toast({ message: 'You can only edit your own routes.', type: 'is-danger', position: 'top-center' })
        this.$router.push('/my-rides')
        return
      }
      this.form = {
        start_location: route.start_location,
        destination: route.destination,
        date: route.date,
        time: route.time,
        car_model: route.car_model,
        capacity: route.capacity,
        description: route.description || '',
      }
    } catch (error) {
      toast({ message: 'Failed to load route.', type: 'is-danger', position: 'top-center' })
      this.$router.push('/my-rides')
    } finally {
      this.loading = false
    }
  },
  methods: {
    async submitForm() {
      if (!this.form.start_location.trim()) {
        toast({ message: 'Starting location is required', type: 'is-warning', position: 'top-center' })
        return
      }
      if (!this.form.destination.trim()) {
        toast({ message: 'Destination is required', type: 'is-warning', position: 'top-center' })
        return
      }
      if (this.form.capacity < 1 || this.form.capacity > 50) {
        toast({ message: 'Capacity must be between 1 and 50', type: 'is-warning', position: 'top-center' })
        return
      }

      this.submitting = true
      try {
        const id = this.$route.params.id
        const formData = {
          ...this.form,
          capacity: parseInt(this.form.capacity, 10),
        }
        await axios.patch(`/api/routes/${id}/`, formData, getCSRFConfig())
        toast({ message: 'Route updated successfully!', type: 'is-success', position: 'top-center' })
        this.$router.push('/my-rides')
      } catch (error) {
        const message =
          error.response?.data?.detail ||
          JSON.stringify(error.response?.data) ||
          'Error updating route'
        toast({ message, type: 'is-danger', position: 'top-center' })
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>
