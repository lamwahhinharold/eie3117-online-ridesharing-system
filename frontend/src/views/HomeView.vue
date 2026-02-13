<template>
  <div>
    <!-- Hero banner -->
    <section class="hero is-link is-small mb-5">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-3">
            <i class="fas fa-route mr-2"></i> Available Routes
          </h1>
          <p class="subtitle is-6">Find a shared ride that works for you</p>
        </div>
      </div>
    </section>

    <div class="container">
      <!-- Search & filter bar -->
      <div class="box mb-5">
        <div class="columns is-vcentered">
          <div class="column is-5">
            <div class="field has-addons">
              <div class="control has-icons-left is-expanded">
                <input class="input" type="text" placeholder="Search routes..." v-model="searchQuery">
                <span class="icon is-left"><i class="fas fa-search"></i></span>
              </div>
            </div>
          </div>
          <div class="column is-3">
            <div class="field">
              <div class="control has-icons-left">
                <div class="select is-fullwidth">
                  <select v-model="filterStatus">
                    <option value="all">All Routes</option>
                    <option value="available">Available Only</option>
                    <option value="expired">Expired Only</option>
                  </select>
                </div>
                <span class="icon is-left"><i class="fas fa-filter"></i></span>
              </div>
            </div>
          </div>
          <div class="column is-4 has-text-right">
            <span class="tag is-info is-light is-medium">
              <i class="fas fa-car mr-2"></i> {{ filteredRoutes.length }} route{{ filteredRoutes.length !== 1 ? 's' : '' }} found
            </span>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large has-text-link">
          <i class="fas fa-spinner fa-pulse fa-2x"></i>
        </span>
        <p class="mt-3 has-text-grey">Loading routes...</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredRoutes.length === 0" class="has-text-centered py-6">
        <span class="icon is-large has-text-grey-light">
          <i class="fas fa-road fa-3x"></i>
        </span>
        <p class="mt-4 is-size-5 has-text-grey">No routes found</p>
        <p class="has-text-grey-light" v-if="searchQuery || filterStatus !== 'all'">Try adjusting your search or filters</p>
        <p class="has-text-grey-light" v-else>Check back soon for new rides!</p>
      </div>

      <!-- Route cards -->
      <template v-else>
        <div class="columns is-multiline">
          <div class="column is-4" v-for="route in filteredRoutes" :key="route.id">
            <div class="card" :class="{ 'has-background-warning-light': isExpired(route) }" style="height: 100%; display: flex; flex-direction: column;">
              <div class="card-content" style="flex: 1;">
                <!-- Header with status -->
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
                  <span v-else-if="!route.is_available" class="tag is-danger">
                    <i class="fas fa-ban mr-1"></i> Full
                  </span>
                  <span v-else class="tag is-success">
                    <i class="fas fa-check mr-1"></i> Available
                  </span>
                </div>

                <!-- Info rows -->
                <div class="is-size-7 has-text-grey mb-3">
                  <p><i class="fas fa-user mr-2 has-text-info"></i> {{ route.driver_name }}</p>
                  <p><i class="fas fa-calendar mr-2 has-text-info"></i> {{ formatDate(route.date) }}</p>
                  <p><i class="fas fa-clock mr-2 has-text-info"></i> {{ route.time }}</p>
                  <p><i class="fas fa-car mr-2 has-text-info"></i> {{ route.car_model }}</p>
                </div>

                <!-- Seat capacity bar -->
                <div>
                  <div class="is-flex is-justify-content-space-between is-size-7 mb-1">
                    <span><strong>Seats</strong></span>
                    <span>{{ route.remaining_seats }} / {{ route.capacity }} left</span>
                  </div>
                  <progress
                    class="progress is-small"
                    :class="seatBarClass(route)"
                    :value="route.remaining_seats"
                    :max="route.capacity">
                  </progress>
                </div>
              </div>
              <footer class="card-footer">
                <router-link :to="{ name: 'RouteDetail', params: { id: route.id } }"
                  class="card-footer-item has-text-link">
                  <i class="fas fa-eye mr-1"></i> View Details
                </router-link>
              </footer>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <nav v-if="totalPages > 1" class="pagination is-centered mt-5" role="navigation" aria-label="pagination">
          <a class="pagination-previous" :disabled="!prevPage" @click="goToPage(currentPage - 1)">
            <i class="fas fa-chevron-left mr-1"></i> Previous
          </a>
          <a class="pagination-next" :disabled="!nextPage" @click="goToPage(currentPage + 1)">
            Next <i class="fas fa-chevron-right ml-1"></i>
          </a>
          <ul class="pagination-list">
            <li v-for="page in totalPages" :key="page">
              <a class="pagination-link" :class="{ 'is-current': page === currentPage }" @click="goToPage(page)">
                {{ page }}
              </a>
            </li>
          </ul>
        </nav>
      </template>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      routes: [],
      loading: true,
      currentPage: 1,
      totalPages: 1,
      nextPage: null,
      prevPage: null,
      searchQuery: '',
      filterStatus: 'all',
    }
  },
  computed: {
    filteredRoutes() {
      let result = this.routes
      // Text search
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase()
        result = result.filter(r =>
          r.start_location.toLowerCase().includes(q) ||
          r.destination.toLowerCase().includes(q) ||
          r.driver_name.toLowerCase().includes(q) ||
          r.car_model.toLowerCase().includes(q)
        )
      }
      // Status filter
      if (this.filterStatus === 'available') {
        result = result.filter(r => !this.isExpired(r) && r.is_available)
      } else if (this.filterStatus === 'expired') {
        result = result.filter(r => this.isExpired(r))
      }
      return result
    },
  },
  mounted() {
    this.getRoutes()
  },
  methods: {
    async getRoutes(page = 1) {
      this.loading = true
      try {
        const response = await axios.get('/api/routes/', { params: { page } })
        const data = response.data
        if (data.results) {
          this.routes = data.results
          this.nextPage = data.next
          this.prevPage = data.previous
          this.totalPages = Math.ceil(data.count / 20) || 1
          this.currentPage = page
        } else {
          this.routes = data
        }
      } catch (error) {
        console.error('Error fetching routes:', error)
        const { toast } = await import('bulma-toast')
        toast({ message: 'Failed to load routes. Please try again.', type: 'is-danger', position: 'top-center' })
      } finally {
        this.loading = false
      }
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.getRoutes(page)
      }
    },
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
    }
  }
}
</script>