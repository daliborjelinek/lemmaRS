import API from "@/model/httpclient.js"
import {createHelpers} from "vuex-map-fields";


const {getResField, updateResField} = createHelpers({
    getterType: 'getResField',
    mutationType: 'updateResField',
});

const state = {
    resources: [],
    selectedResources: [],

    tag: null,
    search: '',
    reservationDate: [],
    unavailable: false,
    disallowed: true,
    project: null,
};

const getters = {
    getResField,
    filteredResources: (state, getters, rootState) => {
        return state.resources.filter(res => {
            const tag = state.tag ? res.tags.includes(state.tag) : true
            let search = true;
            if (state.search) {

                search = res.name.toLowerCase().includes(state.search.toLowerCase())
            }

            return tag && search
            //const searchName = state.search ? res.name.includes(state.filters.search) : true
            //const searchTag =  state.search ? res.name.includes(state.filters.search) : true


        }).map(res => {
            res.selected = state.selectedResources.includes(res)
            res.allowed = rootState.user.profile.permission_level >= res.required_permission_level
            return res
        }
        );
    },
    filteredResourcesCount: (state, getters, rootState) => {
        return getters.filteredResources.length
    }
};

const actions = {
    async getResources({commit, dispatch}) {
        const resources = await API.getResources()
        commit('setResources', resources)

    }
};

const mutations = {
    updateResField,
    setResources: (state, resources) => {
        state.resources = resources
    },
    setTagFilter(state, value) {
        state.tag = value
    },
    setSearch(state, value) {
        state.search = value
    },
    toggleSelectedItem(state, resource){
        if (state.selectedResources.includes(resource)){
            state.selectedResources = state.selectedResources.filter(itm => resource !== itm)
        } else state.selectedResources.push(resource)
        console.log(state.selectedResources)
    },
    removeSelectedItem(state,resource) {
        state.selectedResources = state.selectedResources.filter(itm => itm !== resource)
    }
    }
;

export default {
    state,
    getters,
    actions,
    mutations
};
