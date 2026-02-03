<template>
  <div class="container">
    <h1 class="title">My Rides</h1>

    <div v-if="!$store.state.user.is_driver">
      <h2 class="subtitle">Routes I've Reserved</h2>
      <div v-if="bookings.length === 0" class="notification">You haven't reserved any rides yet.</div>
      <div class="columns is-multiline">
        <div class="column is-12" v-for="booking in bookings" :key="booking.id">
          <div class="card">
            <div class="card-content">
              <p class="title is-5">{{ booking.route_details.start_location }} → {{ booking.route_details.destination }}</p>
              <p class="subtitle is-6">{{ booking.route_details.date }} at {{ booking.route_details.time }}</p>
              <p><strong>Driver:</strong> {{ booking.route_details.driver_name }}</p>
              <p><strong>Car:</strong> {{ booking.route_details.car_model }}</p>
            </div>
            <footer class="card-footer">
              <router-link :to="{ name: 'RouteDetail', params: { id: booking.route_details.id } }" class="card-footer-item">View Details</router-link>
              <a @click="cancelBooking(booking.id)" class="card-footer-item has-text-danger">Cancel Reservation</a>
            </footer>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <h2 class="subtitle">Routes I'm Driving</h2>
      <div v-if="myRoutes.length === 0" class="notification">You haven't advertised any routes yet.</div>
      <div class="columns is-multiline">
        <div class="column is-12" v-for="route in myRoutes" :key="route.id">
          <div class="card mb-4">
            <header class="card-header">
              <p class="card-header-title">
                {{ route.start_location }} to {{ route.destination }} ({{ route.date }})
              </p>
            </header>
            <div class="card-content">
              <p><strong>Time:</strong> {{ route.time }}</p>
              <p><strong>Car Model:</strong> {{ route.car_model }}</p>
              <p><strong>Capacity:</strong> {{ route.remaining_seats }} / {{ route.capacity }} seats available</p>
              <p><strong>Passengers:</strong></p>
              <ul v-if="route.passengers && route.passengers.length">
                <li v-for="pname in route.passengers" :key="pname">{{ pname }}</li>
              </ul>
              <p v-else class="is-italic">No passengers joined yet.</p>
            </div>
            <footer class="card-footer">
              <router-link :to="{ name: 'RouteDetail', params: { id: route.id } }" class="card-footer-item">View Details</router-link>
            </footer>
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
      bookings: [], // for riders
      myRoutes: []  // for drivers
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        if (this.$store.state.user.is_driver) {
          const response = await axios.get('/api/routes/my_advertisements/')
          this.myRoutes = response.data
        } else {
          const response = await axios.get('/api/bookings/')
          this.bookings = response.data
        }
      } catch (error) {
        console.error("Error fetching data", error)
      }
    },
    async cancelBooking(id) {
      if (confirm('Are you sure you want to cancel this reservation?')) {
        try {
          await axios.delete(`/api/bookings/${id}/`, getCSRFConfig())
          toast({ message: 'Reservation cancelled', type: 'is-info' })
          this.fetchData()
        } catch (error) {
          toast({ message: error.response?.data?.detail || 'Error cancelling', type: 'is-danger' })
        }
      }
    }
  }
}
</script>