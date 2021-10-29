import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import vuetify from './plugins/vuetify';
import '@babel/polyfill'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import '@fortawesome/fontawesome-free/css/all.css'
import PortalVue from 'portal-vue'
import axios from 'axios';
import VueMomentJS from "vue-momentjs";
import vueDebounce from "vue-debounce"
import VueLazyImageLoading from 'vue-lazy-image-loading'
import VueRandomColor from 'vue-randomcolor'

import Moment from 'moment';
import { extendMoment } from 'moment-range';

const moment = extendMoment(Moment);

document.title = 'Rezervační systém LEMMA'

export const HTTP = axios.create({
  baseURL: process.env.ROOT_API
})

Vue.use(PortalVue)
Vue.use(vueDebounce)
Vue.use(VueMomentJS, moment);
Vue.use(VueLazyImageLoading);
Vue.use(VueRandomColor)

Vue.config.productionTip = false


new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')




