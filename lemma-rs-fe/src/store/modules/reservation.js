import API from "@/model/httpclient.js"
import {createHelpers} from "vuex-map-fields";
import Moment from 'moment';
import { extendMoment } from 'moment-range';
const moment = extendMoment(Moment);

const {getResField, updateResField} = createHelpers({
    getterType: 'getResField',
    mutationType: 'updateResField',
});
function initState(){
    return {

        selectedResources: [],
        startTime: null,
        endTime: null,
        startDate: null,
        endDate: null,
        reservationDate: [],
        project: null,
    }
}

const state = {
    resources: [],
    selectedResources: [],
    startTime: null,
    endTime: null,
    startDate: null,
    endDate: null,
    tag: 2,
    search: '',
    reservationDate: [],
    provider: null,
    alreadyReserved: false,
    disallowed: true,
    inactive: false,
    project: null,
}

const getters = {
    getResField,
    reservationRange: (state) => {
        const startDateTime = moment(state.startDate + ' '+ state.startTime).toISOString()
        const endDateTime = moment(state.endDate + ' ' + state.endTime).toISOString()
        return {
            startDateTime,
            endDateTime,
            range: moment.range(moment(startDateTime),moment(endDateTime))
        }
    },
    reservationErrors: (state, getters, rootState) => {
        const errors = {
            timeConflicts: [],
            invalidProvider: [],
        }
        state.selectedResources.forEach(res =>{
            if(res.hasTimeConflict) errors.timeConflicts.push()
            if(res.provider !== state.provider) errors.invalidProvider.push()
        })
        errors.reservationIsValid = errors.timeConflicts.length + errors.invalidProvider.length === 0
        return errors

    },
    filteredResources: (state, getters, rootState) => {
        return state.resources.map(res => {
                res.selected = state.selectedResources.includes(res)
                res.allowed = rootState.user.profile.permission_level >= res.required_permission_level
                res.providerStr = rootState.providers.find(x => x.id === res.provider)?.fullname
                res.hasTimeConflict = res.blocking_reservations.find((br) =>{
                   const isOverlap =  moment.range(moment(br.start),moment((br.end))).overlaps(getters.reservationRange.range)

                    if(isOverlap){
                        console.log('conflict with:', br)
                        return true
                    } else return false

                })
                res.reservationIsPossible = res.active && res.allowed && !res.hasTimeConflict && res.provider === state.provider
                return res
            }
        ).filter(res => {
            const tag = state.tag ? res.tags.includes(state.tag) : true
            let search = true;
            let notReserved = true;
            let activity = true;
            let permission = true;
            if (state.search) {
                search = res.name.toLowerCase().includes(state.search.toLowerCase())
            }
            if (!state.inactive) activity =  res.active
            if (!state.disallowed) permission = res.allowed
            if (!state.alreadyReserved) notReserved = !res.hasTimeConflict
            return tag && search && activity && permission && notReserved
            //const searchName = state.search ? res.name.includes(state.filters.search) : true
            //const searchTag =  state.search ? res.name.includes(state.filters.search) : true


        });
    },
    filteredResourcesCount: (state, getters, rootState) => {
        return getters.filteredResources.length
    },
    totalCost: (state, getters) => {
        return state.selectedResources.reduce((acc,itm) => acc + itm.cost,0)
    },
    reservationLength: (state) => {
        if(state.startDate && state.endDate) return moment(state.endDate).diff(moment(state.startDateDate),'days')+1
        return 0
    },
    hourCost(state,getters){
        return getters.totalCost/1000 * getters.reservationLength *24
    },
    approvalRequired(state,getters){
        return  getters.hourCost > 50000
    },
    reservationIsValid: (state, getters) =>{
       return true
    }
};

const actions = {
    async getResources({commit, dispatch}) {
        const resources = await API.getResources()
        commit('setResources', resources)

    },
    async sendReservation({commit, dispatch, state, getters},) {
        const resources = state.selectedResources.map(res => res.id)
        const approvalRequired = getters.approvalRequired
        await API.createReservation(getters.reservationRange.startDateTime,getters.reservationRange.endDateTime,resources,approvalRequired,state.project)
        dispatch('getResources')
        commit('flushReservation')
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
    },
    setTime(state,{time,type}){
        if(type==='start') state.startTime=time
        if(type==='end') state.endTime=time
    },
    setDate(state,{start, end}) {
        state.startDate = start
        state.endDate = end
    },
    setProject(state,project){
        state.project = project
    },
    flushReservation(state){
            // acquire initial state
            const s = initState()
            Object.keys(s).forEach(key => {
                state[key] = s[key]
            })
    },
    }
;

export default {
    state,
    getters,
    actions,
    mutations
};
