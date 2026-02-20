<template>
  <div>
    <section class="page-hero">
      <div class="container">
        <h1 class="title"><i class="fas fa-pen-to-square mr-2"></i> Edit Route</h1>
        <p class="subtitle">Update your ride details</p>
      </div>
    </section>

    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="has-text-centered py-6">
        <span class="icon is-large" style="color: var(--primary);"><i class="fas fa-spinner fa-pulse fa-2x"></i></span>
        <p class="mt-3" style="color: var(--text-secondary);">Loading route…</p>
      </div>

      <div v-else class="columns is-centered">
        <div class="column is-7">
          <RouteForm
            :initial-data="routeData"
            :is-editing="true"
            :loading="submitting"
            @submit="handleUpdate"
            @cancel="goBack"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { toast } from 'bulma-toast'
import { getCSRFConfig } from '../utils/auth'
import RouteForm from '../components/RouteForm.vue'

export default {
  components: { RouteForm },
  data() {
    return {
      loading: true,
      submitting: false,
      routeData: {
        start_location: '',
        destination: '',
        date: '',
        time: '',
        car_model: '',
        capacity: 1,
        description: '',
      },
    }
  },
  async mounted() {
    const id = this.$route.params.id
    try {
      const response = await axios.get(`/api/routes/${id}/`)
      const route = response.data
      if (route.driver !== this.$store.state.user.id) {
        toast({ message: 'You can only edit your own routes.', type: 'is-danger', position: 'top-center' })
        this.$router.push('/my-rides')
        return
      }
      this.routeData = {
        start_location: route.start_location,
        destination: route.destination,
        date: route.date,
        time: route.time,
        car_model: route.car_model,
        capacity: route.capacity,
        description: route.description || '',
      }
    } catch (error) {
      toast({ message: 'Failed to load route.', type: 'is-danger', position: 'top-center' })
      this.$router.push('/my-rides')
    } finally {
      this.loading = false
    }
  },
  methods: {
    goBack() {
      this.$router.push('/my-rides')
    },
    async handleUpdate(formData) {
      this.submitting = true
      try {
        const id = this.$route.params.id
        await axios.patch(`/api/routes/${id}/`, formData, getCSRFConfig())
        toast({ message: 'Route updated successfully!', type: 'is-success', position: 'top-center' })
        this.$router.push('/my-rides')
      } catch (error) {
        const message =
          error.response?.data?.detail ||
          JSON.stringify(error.response?.data) ||
          'Error updating route'
        toast({ message, type: 'is-danger', position: 'top-center' })
      } finally {
        this.submitting = false
      }
    },
  },
}
</script>
