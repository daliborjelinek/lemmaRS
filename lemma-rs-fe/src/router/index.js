import Vue from 'vue'
import VueRouter from 'vue-router'
import Resources from '../views/Reservation.vue'
import Projects from '../views/Projects/Projects.vue'
import User from '../views/User.vue'
import Login from '@/views/Login.vue'
import Test from '@/views/Test.vue'
import qs from 'qs'
import store from '@/store'
import Reservations from "@/views/Reservations";
import Permissions from "@/views/Permissions";


Vue.use(VueRouter)


const ifAuthenticated = (to, from, next) => {
  if (localStorage.getItem('user-token')) {
    next();
    return;
  }
  next("/login");
};

const ifNotAuthenticated = (to, from, next) => {
  if (!localStorage.getItem('user-token')) {
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
    path: '/Reservations',
    name: 'Reservations',
    component: Reservations,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/Permissions',
    name: 'Permissions',
    component: Permissions,
    beforeEnter: ifAuthenticated
  },
  {
    path: '/Test',
    name: 'Test',
    component: Test,
  },
  {
    path: '/auth/signinwin/main/',
    name: 'Auth',
    async beforeEnter(to,from,next) {
      const code = to.query.code
      console.log(code,to)
      window.opener.postMessage({ code }, window.location.origin)
      console.log(code)
      window.close();
    }
  },
  {
    path: '/auth/callback/',
    name: 'Auth1',
    async beforeEnter(to,from,next) {
      const token = qs.parse(to.hash.slice(1)).access_token
      window.opener.postMessage({ token }, window.location.origin)
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
})




export default router
