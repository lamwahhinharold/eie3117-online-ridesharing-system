<template>
  <div>
    <!-- Hero -->
    <section class="page-hero">
      <div class="container">
        <h1 class="title">
          <i class="fas" :class="$store.state.user.is_driver ? 'fa-route' : 'fa-suitcase-rolling'" style="margin-right:.5rem"></i>
          {{ $store.state.user.is_driver ? 'My Routes' : 'My Rides' }}
        </h1>
        <p class="subtitle">{{ $store.state.user.is_driver ? 'Routes you\'re driving' : 'Your reserved rides' }}</p>
      </div>
    </section>

    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large" style="color: var(--primary);"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
        <p class="mt-3" style="color: var(--text-secondary);">{{ $store.state.user.is_driver ? 'Loading your routes…' : 'Loading your rides…' }}</p>
      </div>

      <DriverDashboard
        v-else-if="$store.state.user.is_driver"
        :routes="myRoutes"
        @delete="fetchData"
      />

      <RiderDashboard
        v-else
        :bookings="bookings"
        @cancel="fetchData"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import DriverDashboard from '../components/DriverDashboard.vue'
import RiderDashboard from '../components/RiderDashboard.vue'

export default {
  components: { DriverDashboard, RiderDashboard },
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
  }
}
</script>