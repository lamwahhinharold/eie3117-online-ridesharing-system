/**
 * Shared utility functions for route display logic.
 * Used across HomeView, MyRidesView, and RouteDetailView.
 */

/**
 * Check if a route's date/time is in the past.
 * @param {Object} route - Route object with `date` and `time` fields
 * @returns {boolean}
 */
export function isExpired(route) {
  if (!route) return false
  const now = new Date()
  const routeDateTime = new Date(`${route.date}T${route.time}`)
  return routeDateTime < now
}

/**
 * Return a Bulma progress-bar class based on remaining seat ratio.
 * @param {Object} route - Route object with `remaining_seats` and `capacity`
 * @returns {string}
 */
export function seatBarClass(route) {
  const ratio = route.remaining_seats / route.capacity
  if (ratio === 0) return 'is-danger'
  if (ratio <= 0.3) return 'is-warning'
  return 'is-success'
}

/**
 * Format a date string (YYYY-MM-DD) into a readable form.
 * @param {string} dateString - ISO date string
 * @returns {string}
 */
export function formatDate(dateString) {
  const date = new Date(dateString + 'T00:00:00')
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}
