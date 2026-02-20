<template>
  <div>
    <!-- Loading -->
    <div v-if="!route" class="has-text-centered py-6" style="margin-top: 4rem;">
      <span class="icon is-large" style="color: var(--primary);"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
      <p class="mt-3" style="color: var(--text-secondary);">Loading route details…</p>
    </div>

    <template v-else>
      <!-- Hero with route info -->
      <section class="page-hero">
        <div class="container">
          <router-link to="/" class="back-link">
            <i class="fas fa-arrow-left mr-2"></i> Back to Routes
          </router-link>
          <div class="route-hero-endpoints">
            <div class="route-hero-point">
              <span class="route-hero-dot route-hero-dot--start"></span>
              <span>{{ route.start_location }}</span>
            </div>
            <i class="fas fa-arrow-right route-hero-arrow"></i>
            <div class="route-hero-point">
              <span class="route-hero-dot route-hero-dot--end"></span>
              <span>{{ route.destination }}</span>
            </div>
          </div>
        </div>
      </section>

      <div class="container">
        <div class="columns is-centered">
          <div class="column is-8">
            <div class="box detail-box" :class="{ 'is-expired': isExpired }">
              <!-- Status badge -->
              <div class="has-text-right mb-4">
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

              <!-- Info grid -->
              <div class="columns is-multiline mb-4">
                <div class="column is-6">
                  <div class="detail-item">
                    <div class="detail-item-icon"><i class="fas fa-user"></i></div>
                    <div>
                      <p class="detail-label">Driver</p>
                      <p class="detail-value">{{ route.driver_name }}</p>
                    </div>
                  </div>
                </div>
                <div class="column is-6">
                  <div class="detail-item">
                    <div class="detail-item-icon"><i class="fas fa-car"></i></div>
                    <div>
                      <p class="detail-label">Vehicle</p>
                      <p class="detail-value">{{ route.car_model }}</p>
                    </div>
                  </div>
                </div>
                <div class="column is-6">
                  <div class="detail-item">
                    <div class="detail-item-icon"><i class="fas fa-calendar"></i></div>
                    <div>
                      <p class="detail-label">Date</p>
                      <p class="detail-value">{{ formatDate(route.date) }}</p>
                    </div>
                  </div>
                </div>
                <div class="column is-6">
                  <div class="detail-item">
                    <div class="detail-item-icon"><i class="fas fa-clock"></i></div>
                    <div>
                      <p class="detail-label">Time</p>
                      <p class="detail-value">{{ route.time }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Description -->
              <div class="mb-5" v-if="route.description">
                <p class="detail-label mb-1"><i class="fas fa-align-left mr-1"></i> Description</p>
                <p style="font-size: 0.93rem; line-height: 1.6;">{{ route.description }}</p>
              </div>

              <!-- Seat capacity bar -->
              <div class="mb-5">
                <div class="is-flex is-justify-content-space-between mb-1">
                  <span class="has-text-weight-semibold" style="font-size: 0.9rem;"><i class="fas fa-chair mr-1"></i> Seat Availability</span>
                  <span style="color: var(--text-secondary); font-size: 0.88rem;">{{ route.remaining_seats }} / {{ route.capacity }} remaining</span>
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
    </template>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from '../utils/auth'
import { isExpired as isRouteExpired, seatBarClass as routeSeatBarClass, formatDate } from '../utils/route'

export default {
  data() {
    return { route: null, reserving: false }
  },
  computed: {
    isExpired() {
      return isRouteExpired(this.route)
    },
    seatBarClass() {
      if (!this.route) return ''
      return routeSeatBarClass(this.route)
    },
  },
  mounted() {
    this.getRouteDetail()
  },
  methods: {
    formatDate,
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

<style scoped>
.back-link {
  display: inline-flex;
  align-items: center;
  color: rgba(255,255,255,0.7);
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 1rem;
  transition: color 0.2s ease;
}
.back-link:hover { color: #fff; }

.route-hero-endpoints {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.route-hero-point {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
}
.route-hero-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}
.route-hero-dot--start { background: rgba(255,255,255,0.8); }
.route-hero-dot--end   { background: var(--success); }
.route-hero-arrow {
  color: rgba(255,255,255,0.5);
  font-size: 0.9rem;
}

.detail-box.is-expired {
  opacity: 0.75;
}
.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.detail-item-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius);
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}
.detail-label {
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-bottom: 0.1rem;
}
.detail-value {
  font-weight: 600;
  font-size: 0.95rem;
}
</style>