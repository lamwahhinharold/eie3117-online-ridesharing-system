/**
 * Utility functions for authentication and CSRF handling
 */
import axios from 'axios'

/**
 * Get CSRF token from cookies
 * @param {string} name - Cookie name (default: 'csrftoken')
 * @returns {string|null} - Cookie value or null if not found
 */
export function getCookie(name = 'csrftoken') {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/**
 * Get axios config with CSRF token
 * @returns {Object} - Axios config object with CSRF header
 */
export function getCSRFConfig() {
  return {
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    }
  }
}

/**
 * Ensure CSRF token is fetched before making requests
 * @returns {Promise} - Resolves when CSRF token is fetched
 */
export async function ensureCSRFToken() {
  await axios.get('/api/csrf/')
}
