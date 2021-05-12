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
import { createOidcAuth, SignInType } from 'vue-oidc-client';
import axios from 'axios';
import moment from "moment";
import VueMomentJS from "vue-momentjs";
import vueDebounce from "vue-debounce"
import VueLazyImageLoading from 'vue-lazy-image-loading'



console.log(process.env.NODE_ENV)
document.title = 'Rezervační systém LEMMA'

export const HTTP = axios.create({
  baseURL: process.env.ROOT_API
})


// const appUrl = 'http://localhost:8080/';
//
// // SignInType could be Window or Popup
//  var mainOidc = createOidcAuth('main', SignInType.Window, appUrl , {
//    authority: 'http://localhost:4011/connect/authorize',
//    client_id: 'implicit-mock-client-backup',
//    response_type: 'id_token token',
//    scope: 'openid profile email'
//  });

Vue.use(PortalVue)
Vue.use(vueDebounce)
Vue.use(VueMomentJS, moment);
Vue.use(VueLazyImageLoading)

Vue.config.productionTip = false

// mainOidc.useRouter(router);
//Vue.prototype.$oidc = mainOidc

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')

// mainOidc.startup().then(ok => {
//   if (ok) {
//
//   }
// });



