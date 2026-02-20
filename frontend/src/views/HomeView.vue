<template>
  <div>
    <!-- Page hero -->
    <section class="page-hero">
      <div class="container">
        <h1 class="title">
          <i class="fas fa-compass mr-2"></i> Available Routes
        </h1>
        <p class="subtitle">Find a shared ride that works for you</p>
      </div>
    </section>

    <div class="container">
      <!-- Search & filter bar -->
      <div class="box mb-5">
        <div class="columns is-vcentered is-variable is-4">
          <div class="column is-5">
            <div class="field">
              <div class="control has-icons-left">
                <input class="input" type="text" placeholder="Search by location, driver, or vehicle..." v-model="searchQuery">
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
            <span class="tag is-info is-medium">
              <i class="fas fa-car mr-2"></i> {{ filteredRoutes.length }} route{{ filteredRoutes.length !== 1 ? 's' : '' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large" style="color: var(--primary);">
          <i class="fas fa-spinner fa-pulse fa-2x"></i>
        </span>
        <p class="mt-3" style="color: var(--text-secondary);">Loading routes…</p>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredRoutes.length === 0" class="empty-state">
        <div class="empty-state-icon">
          <i class="fas fa-road"></i>
        </div>
        <p class="empty-state-title">No routes found</p>
        <p class="empty-state-sub" v-if="searchQuery || filterStatus !== 'all'">Try adjusting your search or filters</p>
        <p class="empty-state-sub" v-else>Check back soon for new rides!</p>
      </div>

      <!-- Route cards -->
      <template v-else>
        <div class="columns is-multiline">
          <div class="column is-4" v-for="route in filteredRoutes" :key="route.id">
            <div class="card route-card" :class="{ 'is-expired': isExpired(route) }">
              <div class="card-content">
                <!-- Header with status -->
                <div class="is-flex is-justify-content-space-between is-align-items-start mb-4">
                  <div class="route-endpoints">
                    <p class="route-point">
                      <i class="fas fa-map-marker-alt route-icon route-icon--start"></i>
                      {{ route.start_location }}
                    </p>
                    <p class="route-point">
                      <i class="fas fa-flag-checkered route-icon route-icon--end"></i>
                      {{ route.destination }}
                    </p>
                  </div>
                  <span v-if="isExpired(route)" class="tag is-warning">Expired</span>
                  <span v-else-if="!route.is_available" class="tag is-danger">Full</span>
                  <span v-else class="tag is-success">Available</span>
                </div>

                <!-- Info rows -->
                <div class="route-meta">
                  <span><i class="fas fa-user"></i> {{ route.driver_name }}</span>
                  <span><i class="fas fa-calendar"></i> {{ formatDate(route.date) }}</span>
                  <span><i class="fas fa-clock"></i> {{ formatTime(route.time) }}</span>
                  <span><i class="fas fa-car"></i> {{ route.car_model }}</span>
                </div>

                <!-- Seat capacity bar -->
                <div class="mt-4">
                  <div class="is-flex is-justify-content-space-between mb-1" style="font-size: 0.82rem;">
                    <span class="has-text-weight-semibold">Seats</span>
                    <span style="color: var(--text-secondary);">{{ route.remaining_seats }} / {{ route.capacity }} left</span>
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
                  class="card-footer-item">
                  View Details <i class="fas fa-arrow-right ml-2" style="font-size: 0.75rem;"></i>
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
import { isExpired, seatBarClass, formatDate } from '../utils/route'

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
    isExpired,
    seatBarClass,
    formatDate,
    formatTime(timeStr) {
      if (!timeStr) return ''
      const parts = timeStr.split(':')
      return parts.slice(0, 2).join(':')
    },
  }
}
</script>

<style scoped>
.route-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.route-card .card-content {
  flex: 1;
}
.route-card.is-expired {
  opacity: 0.5;
  filter: grayscale(40%);
}
.route-endpoints {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.route-point {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary);
}
.route-icon {
  width: 16px;
  text-align: center;
  flex-shrink: 0;
  font-size: 0.9rem;
}
.route-icon--start { color: var(--primary); }
.route-icon--end   { color: var(--success); }

.route-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
}
.route-meta i {
  color: var(--text-muted);
  margin-right: 0.35rem;
  width: 14px;
  text-align: center;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 4rem 1rem;
}
.empty-state-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--primary-light);
  color: var(--primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 1.25rem;
}
.empty-state-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.35rem;
}
.empty-state-sub {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
</style>