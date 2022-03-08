import API from "@/model/httpclient.js"
import {createHelpers} from "vuex-map-fields";
import Moment from 'moment';
import {extendMoment} from 'moment-range';

const moment = extendMoment(Moment);

const {getResField, updateResField} = createHelpers({
    getterType: 'getResField',
    mutationType: 'updateResField',
});

function initState() {
    return {

        selectedResources: [],
        startTime: null,
        endTime: null,
        dateRange: [],
        provider: 3,
        reservationDate: [],
        project: null,
    }
}

const state = {
    resources: [],
    selectedResources: [],
    dateRange: [],
    startTime: null,
    endTime: null,
    tag: 2,
    search: '',
    reservationDate: [],
    provider: 3,
    alreadyReserved: false,
    disallowed: false,
    inactive: false,
    project: null,
}
const getters = {
    getResField,
    reservationRange: (state, getters) => {
        if (!(getters.startDate && state.startTime && getters.endDate && state.endTime)) {
            return {
                startDateTime: null,
                endDateTime: null,
                range: null,
            }
        }
        const startDateTime = moment(getters.startDate + ' ' + state.startTime, 'YYYY-MM-DD HH:mm').toISOString()
        const endDateTime = moment(getters.endDate + ' ' + state.endTime, 'YYYY-MM-DD HH:mm').toISOString()
        return {
            startDateTime,
            endDateTime,
            range: moment.range(moment(startDateTime), moment(endDateTime))
        }
    },
    formatedResources: (state, getters, rootState) => {
        return state.resources.map(res => {
                res.selected = state.selectedResources.includes(res.id)
                res.allowed = rootState.user.profile.permission_level >= res.required_permission_level
                res.providerStr = rootState.providers.find(x => x.id === res.provider)?.fullname
                res.hasTimeConflict = getters.reservationRange.range ? !!res.blocking_reservations.find((br) => {
                    return moment.range(moment(br.start), moment((br.end))).overlaps(getters.reservationRange.range)
                }) : false
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
                return res.name.toLowerCase().includes(state.search.toLowerCase()) ||
                    res.tags_str.join(' ').toLowerCase().includes(state.search.toLowerCase())
            }
            if (!state.inactive) activity = res.active
            if (!state.disallowed) permission = res.allowed
            if (!state.alreadyReserved) notReserved = !res.hasTimeConflict
            return tag && activity && permission && notReserved
        });
    },
    selectedResourcesObj: (state, getters) => {
        return getters.formatedResources.filter(res => res.selected)
    },
    reservationErrors: (state, getters, rootState) => {
        const errors = {
            timeConflicts: [],
            invalidProvider: [],
        }
        getters.selectedResourcesObj.forEach(res => {
            if (res.hasTimeConflict) errors.timeConflicts.push(res.id)
            if (res.provider !== state.provider) errors.invalidProvider.push(res.id)
        })
        errors.reservationIsValid = errors.timeConflicts.length + errors.invalidProvider.length === 0
        return errors

    },
    filteredResourcesCount: (state, getters, rootState) => {
        return getters.filteredResources.length
    },
    totalCost: (state, getters) => {
        return getters.selectedResourcesObj.reduce((acc, itm) => acc + itm.cost, 0)
    },
    reservationLength: (state, getters) => {
        if (getters.startDate && getters.endDate) return moment(getters.endDate).diff(moment(getters.startDate), 'days') + 1
        return 0
    },
    hourCost(state, getters) {
        return getters.totalCost / 1000 * getters.reservationLength * 24
    },
    approvalRequired(state, getters) {
        return getters.hourCost > 50000
    },
    startDate(state) {
        return state.dateRange[0]
    },
    endDate(state) {
        return state.dateRange[1] || state.dateRange[0]
    },
    reservationIsFilled(state, getters) {
        return getters.hourCost > 0 &&
            state.startTime &&
            state.endTime &&
            getters.startDate &&
            getters.endDate
    }

};

const actions = {
    async getResources({commit, dispatch}) {
        const resources = await API.getResources()
        commit('setResources', resources)

    },
    async sendReservation({commit, dispatch, state, getters},) {
        const resources = state.selectedResources
        const approvalRequired = getters.approvalRequired
        try {
            await API.createReservation(getters.reservationRange.startDateTime, getters.reservationRange.endDateTime, resources, approvalRequired, state.project, state.provider)
            dispatch('notify', {type: 'success', text: 'Rezervace byla vytvořena'})
        } catch (e) {
            dispatch('notify', {type: 'error', text: 'Vytvoření rezervace se nezdařilo'})
            console.log(e)
        }
        await dispatch('getResources')
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
        toggleSelectedItem(state, resource) {
            if (state.selectedResources.includes(resource.id)) {
                state.selectedResources = state.selectedResources.filter(itm => resource.id !== itm)
            } else state.selectedResources.push(resource.id)
        },
        setSelectedResources(state, resources){
          state.selectedResources = resources
        },
        removeSelectedItem(state, resource) {
            state.selectedResources = state.selectedResources.filter(itm => itm !== resource.id)
        },
        setTime(state, {time, type}) {
            if (type === 'start') state.startTime = time
            if (type === 'end') state.endTime = time
        },
        setDate(state, range) {
            state.dateRange = range
        },
        setProject(state, project) {
            state.project = project
        },
        flushReservation(state) {
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
