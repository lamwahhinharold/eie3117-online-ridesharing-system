<template>
  <div>
    <div v-if="bookings.length === 0" class="has-text-centered py-6">
      <span class="icon is-large has-text-grey-light"><i class="fas fa-ticket-alt fa-3x"></i></span>
      <p class="mt-4 is-size-5 has-text-grey">No reservations yet</p>
      <router-link to="/" class="button is-link is-light mt-3">
        <span class="icon"><i class="fas fa-search"></i></span>
        <span>Browse Routes</span>
      </router-link>
    </div>

    <div v-else class="columns is-multiline">
      <div class="column is-6" v-for="booking in bookings" :key="booking.id">
        <div class="card" :class="{ 'has-background-warning-light': isExpired(booking.route_details) }" style="height: 100%; display: flex; flex-direction: column;">
          <div class="card-content" style="flex: 1;">
            <div class="is-flex is-justify-content-space-between is-align-items-start mb-3">
              <div>
                <p class="title is-5 mb-1">
                  <i class="fas fa-map-marker-alt has-text-link mr-1"></i>
                  {{ booking.route_details.start_location }}
                </p>
                <p class="title is-5 mb-0">
                  <i class="fas fa-flag-checkered has-text-success mr-1"></i>
                  {{ booking.route_details.destination }}
                </p>
              </div>
              <span v-if="isExpired(booking.route_details)" class="tag is-warning">
                <i class="fas fa-clock mr-1"></i> Expired
              </span>
              <span v-else class="tag is-success">
                <i class="fas fa-check mr-1"></i> Confirmed
              </span>
            </div>
            <div class="is-size-7 has-text-grey">
              <p><i class="fas fa-user mr-2 has-text-info"></i> {{ booking.route_details.driver_name }}</p>
              <p><i class="fas fa-calendar mr-2 has-text-info"></i> {{ formatDate(booking.route_details.date) }}</p>
              <p><i class="fas fa-clock mr-2 has-text-info"></i> {{ booking.route_details.time }}</p>
              <p><i class="fas fa-car mr-2 has-text-info"></i> {{ booking.route_details.car_model }}</p>
            </div>
          </div>
          <footer class="card-footer">
            <router-link :to="{ name: 'RouteDetail', params: { id: booking.route_details.id } }" class="card-footer-item has-text-link">
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
