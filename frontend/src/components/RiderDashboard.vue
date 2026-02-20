<template>
  <div>
    <div v-if="bookings.length === 0" class="empty-state">
      <div class="empty-state-icon">
        <i class="fas fa-ticket-alt"></i>
      </div>
      <p class="empty-state-title">No reservations yet</p>
      <router-link to="/" class="button is-link mt-4">
        <span class="icon"><i class="fas fa-search"></i></span>
        <span>Browse Routes</span>
      </router-link>
    </div>

    <div v-else class="columns is-multiline">
      <div class="column is-6" v-for="booking in bookings" :key="booking.id">
        <div class="card dash-card" :class="{ 'is-expired': isExpired(booking.route_details) }">
          <div class="card-content">
            <div class="is-flex is-justify-content-space-between is-align-items-start mb-4">
              <div class="route-endpoints">
                <p class="route-point">
                  <span class="route-dot route-dot--start"></span>
                  {{ booking.route_details.start_location }}
                </p>
                <p class="route-point">
                  <span class="route-dot route-dot--end"></span>
                  {{ booking.route_details.destination }}
                </p>
              </div>
              <span v-if="isExpired(booking.route_details)" class="tag is-warning">Expired</span>
              <span v-else class="tag is-success">Confirmed</span>
            </div>
            <div class="dash-meta">
              <span><i class="fas fa-user"></i> {{ booking.route_details.driver_name }}</span>
              <span><i class="fas fa-calendar"></i> {{ formatDate(booking.route_details.date) }}</span>
              <span><i class="fas fa-clock"></i> {{ booking.route_details.time }}</span>
              <span><i class="fas fa-car"></i> {{ booking.route_details.car_model }}</span>
            </div>
          </div>
          <footer class="card-footer">
            <router-link :to="{ name: 'RouteDetail', params: { id: booking.route_details.id } }" class="card-footer-item">
              <i class="fas fa-eye mr-1"></i> Details
            </router-link>
            <a v-if="!isExpired(booking.route_details)" @click="handleCancel(booking.id)" class="card-footer-item has-text-danger">
              <i class="fas fa-times mr-1"></i> Cancel
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
import { isExpired, formatDate } from '../utils/route'

export default {
  props: {
    bookings: {
      type: Array,
      required: true,
    },
  },
  emits: ['cancel'],
  methods: {
    isExpired,
    formatDate,
    async handleCancel(id) {
      if (confirm('Are you sure you want to cancel this reservation?')) {
        try {
          await axios.delete(`/api/bookings/${id}/`, getCSRFConfig())
          toast({ message: 'Reservation cancelled', type: 'is-info', position: 'top-center' })
          this.$emit('cancel')
        } catch (error) {
          toast({ message: error.response?.data?.detail || 'Error cancelling', type: 'is-danger', position: 'top-center' })
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
