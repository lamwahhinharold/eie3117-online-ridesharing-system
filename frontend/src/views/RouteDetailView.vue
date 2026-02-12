<template>
  <div class="container" v-if="route">
    <div class="columns is-centered">
      <div class="column is-8">
        <div class="box">
          <h1 class="title">{{ route.start_location }} to {{ route.destination }}</h1>
          <hr>
          <div class="content">
            <p><strong>Driver:</strong> {{ route.driver_name }}</p>
            <p><strong>Date & Time:</strong> {{ route.date }} at {{ route.time }}</p>
            <p><strong>Car Model:</strong> {{ route.car_model }}</p>
            <p><strong>Capacity:</strong> {{ route.capacity }} seats total</p>
            <p><strong>Remaining:</strong> {{ route.remaining_seats }} seats available</p>
            <p><strong>Description:</strong> {{ route.description || 'No description provided.' }}</p>
          </div>

          <div class="notification is-warning" v-if="!route.is_available">
            This route is currently full.
          </div>

          <button v-else-if="$store.state.isAuthenticated && !$store.state.user.is_driver" @click="reserveSeat"
            class="button is-primary is-large is-fullwidth">
            Reserve a Seat
          </button>

          <p v-else-if="!$store.state.isAuthenticated" class="has-text-centered">
            Please <router-link to="/login">login</router-link> as a rider to reserve.
          </p>
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
    return { route: null }
  },
  mounted() {
    this.getRouteDetail()
  },
  methods: {
    async getRouteDetail() {
      const id = this.$route.params.id
      try {
        const response = await axios.get(`/api/routes/${id}/`)
        this.route = response.data
      } catch (error) {
        console.error(error)
        const { toast } = await import('bulma-toast')
        toast({ message: 'Route not found or failed to load.', type: 'is-danger' })
      }
    },
    async reserveSeat() {
      try {
        await axios.post(`/api/routes/${this.route.id}/join/`, {}, getCSRFConfig())
        toast({ message: 'Reservation successful!', type: 'is-success' })
        this.getRouteDetail() // Refresh seat count
      } catch (error) {
        toast({
          message: error.response?.data?.error || 'Reservation failed',
          type: 'is-danger'
        })
      }
    }
  }
}
</script>