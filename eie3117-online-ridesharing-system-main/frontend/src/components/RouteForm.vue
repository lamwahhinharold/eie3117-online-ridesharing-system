<template>
  <form @submit.prevent="handleSubmit" class="box">
    <!-- Route endpoints -->
    <div class="form-section-header">
      <div class="form-section-icon"><i class="fas fa-route"></i></div>
      <span>Route</span>
    </div>
    <div class="field">
      <label class="label">Starting Location</label>
      <div class="control has-icons-left">
        <input type="text" class="input" placeholder="e.g. PolyU" v-model="form.start_location" required>
        <span class="icon is-left"><i class="fas fa-map-marker-alt"></i></span>
      </div>
    </div>
    <div class="field">
      <label class="label">Destination</label>
      <div class="control has-icons-left">
        <input type="text" class="input" placeholder="e.g. Mong Kok" v-model="form.destination" required>
        <span class="icon is-left"><i class="fas fa-flag-checkered"></i></span>
      </div>
    </div>

    <hr>

    <!-- Schedule -->
    <div class="form-section-header">
      <div class="form-section-icon"><i class="fas fa-calendar-alt"></i></div>
      <span>Schedule</span>
    </div>
    <div class="columns">
      <div class="column">
        <div class="field">
          <label class="label">Date</label>
          <div class="control has-icons-left">
            <input type="date" class="input" v-model="form.date" required>
            <span class="icon is-left"><i class="fas fa-calendar"></i></span>
          </div>
        </div>
      </div>
      <div class="column">
        <div class="field">
          <label class="label">Time</label>
          <div class="control has-icons-left">
            <input type="time" class="input" v-model="form.time" required>
            <span class="icon is-left"><i class="fas fa-clock"></i></span>
          </div>
        </div>
      </div>
    </div>

    <hr>

    <!-- Vehicle -->
    <div class="form-section-header">
      <div class="form-section-icon"><i class="fas fa-car"></i></div>
      <span>Vehicle</span>
    </div>
    <div class="columns">
      <div class="column">
        <div class="field">
          <label class="label">Car Model</label>
          <div class="control has-icons-left">
            <input type="text" class="input" placeholder="e.g. Toyota Camry" v-model="form.car_model" required>
            <span class="icon is-left"><i class="fas fa-car-side"></i></span>
          </div>
        </div>
      </div>
      <div class="column is-4">
        <div class="field">
          <label class="label">Capacity</label>
          <div class="control has-icons-left">
            <input type="number" class="input" v-model="form.capacity" min="1" max="50" required>
            <span class="icon is-left"><i class="fas fa-users"></i></span>
          </div>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label">Description <span class="has-text-grey has-text-weight-normal">(Optional)</span></label>
      <div class="control">
        <textarea class="textarea" placeholder="Any additional details about the ride..." v-model="form.description"></textarea>
      </div>
    </div>

    <div v-if="isEditing" class="buttons mt-5">
      <button type="submit" class="button is-link is-medium is-expanded" :class="{ 'is-loading': loading }" :disabled="loading">
        <span class="icon"><i class="fas fa-save"></i></span>
        <span>Save Changes</span>
      </button>
      <button type="button" class="button is-light is-medium" @click="$emit('cancel')">
        <span class="icon"><i class="fas fa-times"></i></span>
        <span>Cancel</span>
      </button>
    </div>
    <div v-else class="field mt-5">
      <button class="button is-link is-fullwidth is-medium" :class="{ 'is-loading': loading }" :disabled="loading">
        <span class="icon"><i class="fas fa-paper-plane"></i></span>
        <span>Post Route</span>
      </button>
    </div>
  </form>
</template>

<script>
import { toast } from 'bulma-toast'

export default {
  props: {
    initialData: {
      type: Object,
      default: () => ({
        start_location: '',
        destination: '',
        date: '',
        time: '',
        car_model: '',
        capacity: 4,
        description: '',
      }),
    },
    isEditing: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      form: { ...this.initialData },
    }
  },
  watch: {
    initialData: {
      handler(newVal) {
        this.form = { ...newVal }
      },
      deep: true,
    },
  },
  methods: {
    handleSubmit() {
      if (!this.form.start_location.trim()) {
        toast({ message: 'Starting location is required', type: 'is-warning', position: 'top-center' })
        return
      }
      if (!this.form.destination.trim()) {
        toast({ message: 'Destination is required', type: 'is-warning', position: 'top-center' })
        return
      }
      if (this.form.capacity < 1 || this.form.capacity > 50) {
        toast({ message: 'Capacity must be between 1 and 50', type: 'is-warning', position: 'top-center' })
        return
      }
      this.$emit('submit', {
        ...this.form,
        capacity: parseInt(this.form.capacity, 10),
      })
    },
  },
}
</script>

<style scoped>
.form-section-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1rem;
}
.form-section-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius);
  background: var(--primary-light);
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.82rem;
  flex-shrink: 0;
}
</style>
