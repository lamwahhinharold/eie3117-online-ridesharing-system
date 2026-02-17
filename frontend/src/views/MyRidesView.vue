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