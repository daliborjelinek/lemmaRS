import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import auth from "./modules/auth";
Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  state: {
    toasts: []
  },
  actions:{
     async notify({commit, state}, notification){
      notification.id = state.toasts.length
      notification.open = true
      commit('pushNotification',notification)
      
      await new Promise(resolve => setTimeout(resolve, 3000));
      commit('hideNotification',notification.id)



    }
  },
  mutations: {
    pushNotification (state,notification) {
      state.toasts.push(notification)
      
    },
    hideNotification(state,id){
      state.toasts[id].open = false
    }
  },
  modules: {
    user,
    auth
  },
  strict: debug
});
