<template>
  <div>
    <div v-if="routes.length === 0" class="empty-state">
      <div class="empty-state-icon">
        <i class="fas fa-road"></i>
      </div>
      <p class="empty-state-title">No routes advertised yet</p>
      <router-link to="/advertise" class="button is-link mt-4">
        <span class="icon"><i class="fas fa-plus"></i></span>
        <span>Advertise a Route</span>
      </router-link>
    </div>

    <div v-else class="columns is-multiline">
      <div class="column is-6" v-for="route in routes" :key="route.id">
        <div class="card dash-card" :class="{ 'is-expired': isExpired(route) }">
          <div class="card-content">
            <div class="is-flex is-justify-content-space-between is-align-items-start mb-4">
              <div class="route-endpoints">
                <p class="route-point">
                  <span class="route-dot route-dot--start"></span>
                  {{ route.start_location }}
                </p>
                <p class="route-point">
                  <span class="route-dot route-dot--end"></span>
                  {{ route.destination }}
                </p>
              </div>
              <span v-if="isExpired(route)" class="tag is-warning">Expired</span>
              <span v-else class="tag is-info">Active</span>
            </div>

            <!-- Info -->
            <div class="dash-meta">
              <span><i class="fas fa-calendar"></i> {{ formatDate(route.date) }}</span>
              <span><i class="fas fa-clock"></i> {{ route.time }}</span>
              <span><i class="fas fa-car"></i> {{ route.car_model }}</span>
            </div>

            <!-- Seat bar -->
            <div class="mb-3 mt-4">
              <div class="is-flex is-justify-content-space-between mb-1" style="font-size: 0.82rem;">
                <span class="has-text-weight-semibold">Seats</span>
                <span style="color: var(--text-secondary);">{{ route.remaining_seats }} / {{ route.capacity }} left</span>
              </div>
              <progress class="progress is-small" :class="seatBarClass(route)" :value="route.remaining_seats" :max="route.capacity"></progress>
            </div>

            <!-- Passengers -->
            <div>
              <p class="dash-meta-label">
                <i class="fas fa-users mr-1"></i> Passengers
              </p>
              <div v-if="route.passengers && route.passengers.length" class="mt-1">
                <span v-for="pname in route.passengers" :key="pname" class="tag is-info mr-1 mb-1">
                  <i class="fas fa-user mr-1" style="font-size: 0.65rem;"></i> {{ pname }}
                </span>
              </div>
              <p v-else class="dash-meta-empty">No passengers yet</p>
            </div>
          </div>
          <footer class="card-footer">
            <router-link :to="{ name: 'RouteDetail', params: { id: route.id } }" class="card-footer-item">
              <i class="fas fa-eye mr-1"></i> View
            </router-link>
            <router-link v-if="!isExpired(route)" :to="{ name: 'EditRoute', params: { id: route.id } }" class="card-footer-item has-text-info">
              <i class="fas fa-pen mr-1"></i> Edit
            </router-link>
            <a @click="handleDelete(route.id)" class="card-footer-item has-text-danger">
              <i class="fas fa-trash mr-1"></i> Delete
            </a>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from '../utils/auth'
import { isExpired, seatBarClass, formatDate } from '../utils/route'

export default {
  props: {
    routes: {
      type: Array,
      required: true,
    },
  },
  emits: ['delete'],
  methods: {
    isExpired,
    seatBarClass,
    formatDate,
    async handleDelete(id) {
      if (confirm('Are you sure you want to delete this route? All bookings will also be removed.')) {
        try {
          await axios.delete(`/api/routes/${id}/`, getCSRFConfig())
          toast({ message: 'Route deleted successfully', type: 'is-success', position: 'top-center' })
          this.$emit('delete')
        } catch (error) {
          toast({ message: error.response?.data?.detail || 'Error deleting route', type: 'is-danger', position: 'top-center' })
        }
      }
    },
  },
}
</script>

<style scoped>
.dash-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.dash-card .card-content {
  flex: 1;
}
.dash-card.is-expired {
  opacity: 0.7;
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
.route-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.route-dot--start { background: var(--primary); }
.route-dot--end   { background: var(--success); }
.dash-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem 1rem;
  font-size: 0.82rem;
  color: var(--text-secondary);
}
.dash-meta i {
  color: var(--text-muted);
  margin-right: 0.35rem;
  width: 14px;
  text-align: center;
}
.dash-meta-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-secondary);
}
.dash-meta-empty {
  font-size: 0.82rem;
  font-style: italic;
  color: var(--text-muted);
  margin-top: 0.25rem;
}
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
}
</style>
