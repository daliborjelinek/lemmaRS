import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Reservation.vue'
import Auth from '../views/Auth.vue'
import Login from '@/views/Login.vue'
import qs from 'qs'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/Resources',
    name: 'Home',
    component: Home
  },
  {
    path: '/auth/signinwin/main/',
    name: 'Auth',
    async beforeEnter(to,from,next) {
      const token = qs.parse(to.hash.slice(1)).access_token
      window.opener.postMessage({ token }, 'http://localhost:8080')
      //https://github.com/ljharb/qs/issues/222
      console.log(token)
      window.close();
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  routes,
})


export default router
