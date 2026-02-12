<template>
  <div class="container">
    <h1 class="title">Available Routes</h1>
    <div v-if="routes.length === 0" class="notification has-background-info-light">
      No routes available yet. Check back soon!
    </div>
    <div class="columns is-multiline">
      <div class="column is-4" v-for="route in routes" :key="route.id">
        <div class="card">
          <div class="card-content">
            <p class="title is-5">{{ route.start_location }} → {{ route.destination }}</p>
            <p class="subtitle is-6">Driver: {{ route.driver_name }}</p>
            <p><strong>Date:</strong> {{ formatDate(route.date) }} | <strong>Time:</strong> {{ route.time }}</p>
            <p><strong>Car:</strong> {{ route.car_model }}</p>
            <p><strong>Seats Left:</strong> {{ route.remaining_seats }} / {{ route.capacity }}</p>
          </div>
          <footer class="card-footer">
            <router-link :to="{ name: 'RouteDetail', params: { id: route.id } }"
              class="card-footer-item">View</router-link>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return { routes: [] }
  },
  mounted() {
    this.getRoutes()
  },
  methods: {
    async getRoutes() {
      try {
        const response = await axios.get('/api/routes/')
        this.routes = response.data
      } catch (error) {
        console.error('Error fetching routes:', error)
        const { toast } = await import('bulma-toast')
        toast({ message: 'Failed to load routes. Please try again.', type: 'is-danger' })
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
    }
  }
}
</script>