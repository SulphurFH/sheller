// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/assets/style/reset.css'
import router from './router'
import axios from 'axios'
import { httpConfig } from './api/api.js'
import Qs from 'qs'

// axios.defaults.headers.post['Content-Type'] = 'application/json'
// axios.defaults.withCredentials = true // 允许携带cookie`

Vue.prototype.$axios = axios
Vue.prototype.$httpConfig = httpConfig
Vue.prototype.$qs = Qs

Vue.config.productionTip = false

Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
