import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// base URL for Django API
axios.defaults.baseURL = 'http://localhost:8000'

// Enable cookies to be sent with cross-origin requests (for session persistence)
axios.defaults.withCredentials = true

const app = createApp(App)
app.use(store).use(router).mount('#app')
