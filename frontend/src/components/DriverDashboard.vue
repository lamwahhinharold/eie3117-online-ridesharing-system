<template>
  <div>
    <div v-if="routes.length === 0" class="has-text-centered py-6">
      <span class="icon is-large has-text-grey-light"><i class="fas fa-road fa-3x"></i></span>
      <p class="mt-4 is-size-5 has-text-grey">No routes advertised yet</p>
      <router-link to="/advertise" class="button is-link is-light mt-3">
        <span class="icon"><i class="fas fa-plus"></i></span>
        <span>Advertise a Route</span>
      </router-link>
    </div>

    <div v-else class="columns is-multiline">
      <div class="column is-6" v-for="route in routes" :key="route.id">
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
