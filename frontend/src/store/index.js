import { createStore } from 'vuex'
import axios from 'axios'
import { ensureCSRFToken } from '../utils/auth'

let _authReadyResolve
const authReadyPromise = new Promise((resolve) => {
  _authReadyResolve = resolve
})

const store = createStore({
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
    authChecked: false,
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
    setAuthChecked(state) {
      state.authChecked = true
    },
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        await ensureCSRFToken()
        const res = await axios.get('/api/user/')
        commit('setUser', res.data)
      } catch {
        commit('clearAuth')
      } finally {
        commit('setAuthChecked')
        _authReadyResolve()
      }
    },
  },
})

store.authReady = authReadyPromise

export default store
