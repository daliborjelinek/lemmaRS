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
    startTime: '13:00',
    endTime: '13:00',
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
    formatedResources: (state, getters, rootState) => {
        return state.resources.map(res => {
                res.selected = state.selectedResources.includes(res.id)
                res.allowed = rootState.user.profile.permission_level >= res.required_permission_level
                res.providerStr = rootState.providers.find(x => x.id === res.provider)?.fullname
                res.hasTimeConflict = !!res.blocking_reservations.find((br) =>{
                   return  moment.range(moment(br.start),moment((br.end))).overlaps(getters.reservationRange.range)
                })
                res.reservationIsPossible = res.active && res.allowed && !res.hasTimeConflict && res.provider === state.provider
                return res
            }
        )
    },
    filteredResources: (state, getters, rootState) => {
        return getters.formatedResources.filter(res => {
            const tag = state.tag ? res.tags.includes(state.tag) : true
            let search = true;
            let notReserved = true;
            let activity = true;
            let permission = true;
            if (state.search) {
                search = res.name.toLowerCase().includes(state.search.toLowerCase()) ||
                    res.tags_str.join(' ').toLowerCase().includes(state.search.toLowerCase())
            }
            if (!state.inactive) activity =  res.active
            if (!state.disallowed) permission = res.allowed
            if (!state.alreadyReserved) notReserved = !res.hasTimeConflict
            return tag && search && activity && permission && notReserved
        });
    },
    selectedResourcesObj: (state,getters) => {
      return getters.formatedResources.filter(res => res.selected)
    },
    reservationErrors: (state, getters, rootState) => {
        const errors = {
            timeConflicts: [],
            invalidProvider: [],
        }
        getters.selectedResourcesObj.forEach(res =>{
            if(res.hasTimeConflict) errors.timeConflicts.push(res.id)
            if(res.provider !== state.provider) errors.invalidProvider.push(res.id)
        })
        errors.reservationIsValid = errors.timeConflicts.length + errors.invalidProvider.length === 0
        return errors

    },
    filteredResourcesCount: (state, getters, rootState) => {
        return getters.filteredResources.length
    },
    totalCost: (state, getters) => {
        return getters.selectedResourcesObj.reduce((acc,itm) => acc + itm.cost,0)
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
};

const actions = {
    async getResources({commit, dispatch}) {
        const resources = await API.getResources()
        commit('setResources', resources)

    },
    async sendReservation({commit, dispatch, state, getters},) {
        const resources = state.selectedResources
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
        if (state.selectedResources.includes(resource.id)){
            state.selectedResources = state.selectedResources.filter(itm => resource.id !== itm)
        } else state.selectedResources.push(resource.id)
    },
    removeSelectedItem(state,resource) {
        state.selectedResources = state.selectedResources.filter(itm => itm !== resource.id)
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
