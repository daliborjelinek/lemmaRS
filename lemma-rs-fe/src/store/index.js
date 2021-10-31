import Vue from "vue";
import Vuex from "vuex";
import user from "./modules/user";
import auth from "./modules/auth";
import reservation from "./modules/reservation";
import API from "@/model/httpclient.js"

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
    state: {
        toasts: [],
        projects: [],
        providers: [],
    },
    getters: {
        myProjects: (state, getters) => {
           return state.projects.filter( prj => {
               return (prj.members.find(member => member.id === getters.getProfile.id)) ||
                prj.owner.id === getters.getProfile.id


            })
        },
    },
    actions: {
        async notify({commit, state}, notification) {
            notification.id = state.toasts.length
            notification.open = true
            commit('pushNotification', notification)

            await new Promise(resolve => setTimeout(resolve, 3000));
            commit('hideNotification', notification.id)
        },
        async getProjects({commit, state}) {
            const projects = await API.getProjects()
            commit('setProjects', projects)
        },
        async getProviders({commit, state}) {
            const providers = await API.getUsers('PROVIDER,ADMIN')
            commit('setProvides', providers)
        },
    },
    mutations: {
        pushNotification(state, notification) {
            state.toasts.push(notification)

        },
        hideNotification(state, id) {
            state.toasts[id].open = false
        },
        setProjects(state, projects) {
            state.projects = projects
        },
        setProvides(state, providers) {
            state.providers = providers
        }
    },
    modules: {
        user,
        auth,
        reservation
    },
    strict: debug
});
