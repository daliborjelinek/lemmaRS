import Vue from 'vue'
import VueRouter from 'vue-router'
import Resources from '../views/Reservation.vue'
import Projects from '../views/Projects/Projects.vue'
import User from '../views/User.vue'
import Login from '@/views/Login.vue'
import qs from 'qs'
import store from '@/store'


Vue.use(VueRouter)


const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/login");
};

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const routes = [
  {
    path: '/Login',
    name: 'Login',
    component: Login,
    beforeEnter: ifNotAuthenticated
  },
  {
    path: '/',
    name: 'Resources',
    component: Resources,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/User',
    name: 'User',
    component: User,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/Projests',
    name: 'Projects',
    component: Projects,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/auth/signinwin/main/',
    name: 'Auth',
    async beforeEnter(to,from,next) {
      console.log('tadyyyyyyyyyyyyyyyyyyyyyyyyy')
      const code = to.query.code
      console.log(code,to)
      window.opener.postMessage({ code }, 'http://localhost:8080')
      console.log(code)
      window.close();
    }
  },
  {
    path: '/auth/callback/',
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

// avoid complaining about push to same route
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => {

    if ((err.name !== 'NavigationDuplicated')) {
      throw err;
    } else console.log(err.name)
  })
}

const router = new VueRouter({
  mode: 'history',
  routes,
  base: '/rs/'
})




export default router
