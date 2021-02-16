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


const appUrl = 'http://localhost:8081/';

// SignInType could be Window or Popup
var mainOidc = createOidcAuth('main', SignInType.Window, appUrl , {
  authority: 'https://localhost:8443',
  client_id: 'implicit-mock-client',
  response_type: 'id_token token',
  scope: 'openid'
});

Vue.use(PortalVue)

Vue.config.productionTip = false

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
