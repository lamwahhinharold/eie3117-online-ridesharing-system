<template>
  <div>
    <!-- Hero -->
    <section class="hero is-link is-small mb-5">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-3">
            <i class="fas fa-suitcase-rolling mr-2"></i> My Rides
          </h1>
          <p class="subtitle is-6">{{ $store.state.user.is_driver ? 'Routes you\'re driving' : 'Your reserved rides' }}</p>
        </div>
      </div>
    </section>

    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large has-text-link"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
        <p class="mt-3 has-text-grey">Loading your rides...</p>
      </div>

      <!-- === RIDER VIEW === -->
      <template v-else-if="!$store.state.user.is_driver">
        <div v-if="bookings.length === 0" class="has-text-centered py-6">
          <span class="icon is-large has-text-grey-light"><i class="fas fa-ticket-alt fa-3x"></i></span>
          <p class="mt-4 is-size-5 has-text-grey">No reservations yet</p>
          <router-link to="/" class="button is-link is-light mt-3">
            <span class="icon"><i class="fas fa-search"></i></span>
            <span>Browse Routes</span>
          </router-link>
        </div>

        <div v-else class="columns is-multiline">
          <div class="column is-6" v-for="booking in bookings" :key="booking.id">
            <div class="card" :class="{ 'has-background-warning-light': isExpired(booking.route_details) }" style="height: 100%; display: flex; flex-direction: column;">
              <div class="card-content" style="flex: 1;">
                <div class="is-flex is-justify-content-space-between is-align-items-start mb-3">
                  <div>
                    <p class="title is-5 mb-1">
                      <i class="fas fa-map-marker-alt has-text-link mr-1"></i>
                      {{ booking.route_details.start_location }}
                    </p>
                    <p class="title is-5 mb-0">
                      <i class="fas fa-flag-checkered has-text-success mr-1"></i>
                      {{ booking.route_details.destination }}
                    </p>
                  </div>
                  <span v-if="isExpired(booking.route_details)" class="tag is-warning">
                    <i class="fas fa-clock mr-1"></i> Expired
                  </span>
                  <span v-else class="tag is-success">
                    <i class="fas fa-check mr-1"></i> Confirmed
                  </span>
                </div>
                <div class="is-size-7 has-text-grey">
                  <p><i class="fas fa-user mr-2 has-text-info"></i> {{ booking.route_details.driver_name }}</p>
                  <p><i class="fas fa-calendar mr-2 has-text-info"></i> {{ formatDate(booking.route_details.date) }}</p>
                  <p><i class="fas fa-clock mr-2 has-text-info"></i> {{ booking.route_details.time }}</p>
                  <p><i class="fas fa-car mr-2 has-text-info"></i> {{ booking.route_details.car_model }}</p>
                </div>
              </div>
              <footer class="card-footer">
                <router-link :to="{ name: 'RouteDetail', params: { id: booking.route_details.id } }" class="card-footer-item has-text-link">
                  <i class="fas fa-eye mr-1"></i> Details
                </router-link>
                <a v-if="!isExpired(booking.route_details)" @click="cancelBooking(booking.id)" class="card-footer-item has-text-danger">
                  <i class="fas fa-times mr-1"></i> Cancel
                </a>
              </footer>
            </div>
          </div>
        </div>
      </template>

      <!-- === DRIVER VIEW === -->
      <template v-else>
        <div v-if="myRoutes.length === 0" class="has-text-centered py-6">
          <span class="icon is-large has-text-grey-light"><i class="fas fa-road fa-3x"></i></span>
          <p class="mt-4 is-size-5 has-text-grey">No routes advertised yet</p>
          <router-link to="/advertise" class="button is-link is-light mt-3">
            <span class="icon"><i class="fas fa-plus"></i></span>
            <span>Advertise a Route</span>
          </router-link>
        </div>

        <div v-else class="columns is-multiline">
          <div class="column is-6" v-for="route in myRoutes" :key="route.id">
            <div class="card" :class="{ 'has-background-warning-light': isExpired(route) }" style="height: 100%; display: flex; flex-direction: column;">
              <div class="card-content" style="flex: 1;">
                <div class="is-flex is-justify-content-space-between is-align-items-start mb-3">
                  <div>
                    <p class="title is-5 mb-1">
                      <i class="fas fa-map-marker-alt has-text-link mr-1"></i>
                      {{ route.start_location }}
                    </p>
                    <p class="title is-5 mb-0">
                      <i class="fas fa-flag-checkered has-text-success mr-1"></i>
                      {{ route.destination }}
                    </p>
                  </div>
                  <span v-if="isExpired(route)" class="tag is-warning">
                    <i class="fas fa-clock mr-1"></i> Expired
                  </span>
                  <span v-else class="tag is-info">
                    <i class="fas fa-broadcast-tower mr-1"></i> Active
                  </span>
                </div>

                <!-- Info -->
                <div class="is-size-7 has-text-grey mb-3">
                  <p><i class="fas fa-calendar mr-2 has-text-info"></i> {{ formatDate(route.date) }}</p>
                  <p><i class="fas fa-clock mr-2 has-text-info"></i> {{ route.time }}</p>
                  <p><i class="fas fa-car mr-2 has-text-info"></i> {{ route.car_model }}</p>
                </div>

                <!-- Seat bar -->
                <div class="mb-3">
                  <div class="is-flex is-justify-content-space-between is-size-7 mb-1">
                    <span><strong>Seats</strong></span>
                    <span>{{ route.remaining_seats }} / {{ route.capacity }} left</span>
                  </div>
                  <progress class="progress is-small" :class="seatBarClass(route)" :value="route.remaining_seats" :max="route.capacity"></progress>
                </div>

                <!-- Passengers -->
                <div>
                  <p class="is-size-7 has-text-weight-semibold mb-1">
                    <i class="fas fa-users mr-1 has-text-info"></i> Passengers
                  </p>
                  <div v-if="route.passengers && route.passengers.length">
                    <span v-for="pname in route.passengers" :key="pname" class="tag is-light is-info mr-1 mb-1">
                      <i class="fas fa-user mr-1"></i> {{ pname }}
                    </span>
                  </div>
                  <p v-else class="is-size-7 is-italic has-text-grey">No passengers yet</p>
                </div>
              </div>
              <footer class="card-footer">
                <router-link :to="{ name: 'RouteDetail', params: { id: route.id } }" class="card-footer-item has-text-link">
                  <i class="fas fa-eye mr-1"></i> View
                </router-link>
                <router-link v-if="!isExpired(route)" :to="{ name: 'EditRoute', params: { id: route.id } }" class="card-footer-item has-text-info">
                  <i class="fas fa-pen mr-1"></i> Edit
                </router-link>
                <a @click="deleteRoute(route.id)" class="card-footer-item has-text-danger">
                  <i class="fas fa-trash mr-1"></i> Delete
                </a>
              </footer>
            </div>
          </div>
        </div>
      </template>
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
      bookings: [],
      myRoutes: [],
      loading: true,
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    isExpired(route) {
      if (!route) return false
      const now = new Date()
      const routeDateTime = new Date(`${route.date}T${route.time}`)
      return routeDateTime < now
    },
    seatBarClass(route) {
      const ratio = route.remaining_seats / route.capacity
      if (ratio === 0) return 'is-danger'
      if (ratio <= 0.3) return 'is-warning'
      return 'is-success'
    },
    formatDate(dateString) {
      const date = new Date(dateString + 'T00:00:00')
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
    },
    async fetchData() {
      this.loading = true
      try {
        if (this.$store.state.user.is_driver) {
          const response = await axios.get('/api/routes/my_advertisements/')
          this.myRoutes = response.data.results || response.data
        } else {
          const response = await axios.get('/api/bookings/')
          this.bookings = response.data.results || response.data
        }
      } catch (error) {
        console.error("Error fetching data", error)
      } finally {
        this.loading = false
      }
    },
    async cancelBooking(id) {
      if (confirm('Are you sure you want to cancel this reservation?')) {
        try {
          await axios.delete(`/api/bookings/${id}/`, getCSRFConfig())
          toast({ message: 'Reservation cancelled', type: 'is-info', position: 'top-center' })
          this.fetchData()
        } catch (error) {
          toast({ message: error.response?.data?.detail || 'Error cancelling', type: 'is-danger', position: 'top-center' })
        }
      }
    },
    async deleteRoute(id) {
      if (confirm('Are you sure you want to delete this route? All bookings will also be removed.')) {
        try {
          await axios.delete(`/api/routes/${id}/`, getCSRFConfig())
          toast({ message: 'Route deleted successfully', type: 'is-success', position: 'top-center' })
          this.fetchData()
        } catch (error) {
          toast({ message: error.response?.data?.detail || 'Error deleting route', type: 'is-danger', position: 'top-center' })
        }
      }
    },
  }
}
</script>