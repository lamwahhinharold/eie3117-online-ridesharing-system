<template>
  <div>
    <!-- Loading -->
    <div v-if="!route" class="has-text-centered py-6">
      <span class="icon is-large has-text-link"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
      <p class="mt-3 has-text-grey">Loading route details...</p>
    </div>

    <div v-else class="container">
      <!-- Back button -->
      <div class="mb-4">
        <router-link to="/" class="button is-light is-small">
          <span class="icon"><i class="fas fa-arrow-left"></i></span>
          <span>Back to Routes</span>
        </router-link>
      </div>

      <div class="columns is-centered">
        <div class="column is-8">
          <div class="box" :class="{ 'has-background-warning-light': isExpired }">
            <!-- Route header -->
            <div class="is-flex is-justify-content-space-between is-align-items-start mb-2">
              <div>
                <p class="is-size-6 has-text-grey mb-1">
                  <i class="fas fa-map-marker-alt has-text-link mr-1"></i> From
                </p>
                <h1 class="title is-4 mb-2">{{ route.start_location }}</h1>
                <p class="is-size-6 has-text-grey mb-1">
                  <i class="fas fa-flag-checkered has-text-success mr-1"></i> To
                </p>
                <h1 class="title is-4 mb-0">{{ route.destination }}</h1>
              </div>
              <div>
                <span v-if="isExpired" class="tag is-warning is-medium">
                  <i class="fas fa-clock mr-1"></i> Expired
                </span>
                <span v-else-if="!route.is_available" class="tag is-danger is-medium">
                  <i class="fas fa-ban mr-1"></i> Full
                </span>
                <span v-else class="tag is-success is-medium">
                  <i class="fas fa-check mr-1"></i> Available
                </span>
              </div>
            </div>

            <hr>

            <!-- Info grid -->
            <div class="columns is-multiline mb-4">
              <div class="column is-6">
                <div class="is-flex is-align-items-center mb-3">
                  <span class="icon has-text-link mr-2"><i class="fas fa-user"></i></span>
                  <div>
                    <p class="is-size-7 has-text-grey">Driver</p>
                    <p class="has-text-weight-semibold">{{ route.driver_name }}</p>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="is-flex is-align-items-center mb-3">
                  <span class="icon has-text-link mr-2"><i class="fas fa-car"></i></span>
                  <div>
                    <p class="is-size-7 has-text-grey">Vehicle</p>
                    <p class="has-text-weight-semibold">{{ route.car_model }}</p>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="is-flex is-align-items-center mb-3">
                  <span class="icon has-text-link mr-2"><i class="fas fa-calendar"></i></span>
                  <div>
                    <p class="is-size-7 has-text-grey">Date</p>
                    <p class="has-text-weight-semibold">{{ formatDate(route.date) }}</p>
                  </div>
                </div>
              </div>
              <div class="column is-6">
                <div class="is-flex is-align-items-center mb-3">
                  <span class="icon has-text-link mr-2"><i class="fas fa-clock"></i></span>
                  <div>
                    <p class="is-size-7 has-text-grey">Time</p>
                    <p class="has-text-weight-semibold">{{ route.time }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Description -->
            <div class="mb-4" v-if="route.description">
              <p class="is-size-7 has-text-grey mb-1"><i class="fas fa-align-left mr-1"></i> Description</p>
              <p>{{ route.description }}</p>
            </div>

            <!-- Seat capacity bar -->
            <div class="mb-5">
              <div class="is-flex is-justify-content-space-between mb-1">
                <span class="has-text-weight-semibold"><i class="fas fa-chair mr-1"></i> Seat Availability</span>
                <span>{{ route.remaining_seats }} / {{ route.capacity }} remaining</span>
              </div>
              <progress class="progress" :class="seatBarClass" :value="route.remaining_seats" :max="route.capacity"></progress>
            </div>

            <!-- CTA section -->
            <div class="notification is-warning is-light" v-if="isExpired">
              <i class="fas fa-exclamation-triangle mr-2"></i> This route has expired and can no longer be booked.
            </div>

            <div class="notification is-danger is-light" v-else-if="!route.is_available">
              <i class="fas fa-ban mr-2"></i> This route is currently full. Check back later for cancellations.
            </div>

            <button v-else-if="$store.state.isAuthenticated && !$store.state.user.is_driver" @click="reserveSeat"
              class="button is-link is-medium is-fullwidth" :class="{ 'is-loading': reserving }" :disabled="reserving">
              <span class="icon"><i class="fas fa-ticket-alt"></i></span>
              <span>Reserve a Seat</span>
            </button>

            <div v-else-if="!$store.state.isAuthenticated" class="notification is-info is-light has-text-centered">
              <i class="fas fa-sign-in-alt mr-2"></i>
              Please <router-link to="/login" class="has-text-weight-semibold">login</router-link> as a rider to reserve a seat.
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
    return { route: null, reserving: false }
  },
  computed: {
    isExpired() {
      if (!this.route) return false
      const now = new Date()
      const routeDateTime = new Date(`${this.route.date}T${this.route.time}`)
      return routeDateTime < now
    },
    seatBarClass() {
      if (!this.route) return ''
      const ratio = this.route.remaining_seats / this.route.capacity
      if (ratio === 0) return 'is-danger'
      if (ratio <= 0.3) return 'is-warning'
      return 'is-success'
    },
  },
  mounted() {
    this.getRouteDetail()
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString + 'T00:00:00')
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
    },
    async getRouteDetail() {
      const id = this.$route.params.id
      try {
        const response = await axios.get(`/api/routes/${id}/`)
        this.route = response.data
      } catch (error) {
        console.error(error)
        toast({ message: 'Route not found or failed to load.', type: 'is-danger', position: 'top-center' })
      }
    },
    async reserveSeat() {
      this.reserving = true
      try {
        await axios.post(`/api/routes/${this.route.id}/join/`, {}, getCSRFConfig())
        toast({ message: 'Reservation successful!', type: 'is-success', position: 'top-center' })
        this.getRouteDetail()
      } catch (error) {
        toast({
          message: error.response?.data?.error || 'Reservation failed',
          type: 'is-danger',
          position: 'top-center',
        })
      } finally {
        this.reserving = false
      }
    }
  }
}
</script>