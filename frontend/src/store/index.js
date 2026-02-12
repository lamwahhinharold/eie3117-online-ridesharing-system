import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    user: {
      id: null,
      username: '',
      nickname: '',
      email: '',
      is_driver: false,
      profile_image: null,
    },
    isAuthenticated: false,
  },
  mutations: {
    initializeStore(state) {
      // Session-based auth: no need to check localStorage
      // Authentication status will be verified with server
      state.isAuthenticated = false
    },
    setAuthenticated(state, status) {
      state.isAuthenticated = status
    },
    setUser(state, user) {
      state.user = user
      state.isAuthenticated = true
    },
    clearAuth(state) {
      state.user = {
        id: null,
        username: '',
        nickname: '',
        email: '',
        is_driver: false,
        profile_image: null,
      }
      state.isAuthenticated = false
    },
  },
})
