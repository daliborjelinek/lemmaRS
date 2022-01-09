import axios from 'axios'
import store from '@/store'
import {AUTH_LOGOUT} from "@/store/actions/auth";
import router from '@/router';
import jwt_decode from "jwt-decode";


export const AXIOS = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    headers: {}
})

AXIOS.interceptors.request.use(async (config) => {
    let accessToken = localStorage.getItem('user-token');
    const refreshToken = localStorage.getItem('refresh-token')
    if (accessToken && refreshToken) {
        const atExpiration = jwt_decode(accessToken).exp
        const rtExpiration = jwt_decode(refreshToken).exp
        const currentTime = new Date().getTime() / 1000;
        if ((atExpiration < currentTime) && (rtExpiration > currentTime)) {
            console.log("obtain new token")
            const response = await axios.post(process.env.VUE_APP_API_URL + "/token/refresh/", {
                refresh: refreshToken
            })
            console.log(response)
            accessToken = response.data.access
            localStorage.setItem('user-token', accessToken)
        }
        config.headers['Authorization'] = 'Bearer ' + accessToken;
    }

    return config
})


AXIOS.interceptors.response.use(undefined, async (err) => {

    if (err.response?.status === 401) {

        store.dispatch(AUTH_LOGOUT)
        router.push({name: 'Login'})
        localStorage.removeItem('user-token');
        localStorage.removeItem('refresh-token');

    }
    return Promise.reject(err);

});


//Add a response interceptor


export default {
    async commonGetRequest(query){
      return (await AXIOS.get(query)).data
    },

    async getUsers(roles = null) {
        const q = 'user/' + (roles ? '?role__in=' + roles : '')
        return (await AXIOS.get(q)).data
    },
    // USER
    async getCurentUser() {
        return (await AXIOS.get('user/current/')).data
    },
    async putUser(user) {
        return AXIOS.put('user/' + user.id + '/', user)
    },
    // PROJECT
    async getProjects() {
        return (await AXIOS.get('project/')).data
    },
    async createProject(project) {
        return (await AXIOS.post('project/', project)).data
    },
    async updateProject(project) {
        return AXIOS.put('project/' + project.id + '/', project)
    },
    async addProjectMember(projectId, memberId) {
        return AXIOS.put('project/' + projectId + '/add_member/?userId=' + memberId)
    },
    async removeProjectMember(projectId, memberId) {
        return AXIOS.delete('project/' + projectId + '/remove_member/?userId=' + memberId)
    },

    // PROJECT GROUP
    async getProjectGroups() {
        return (await AXIOS.get('project-group/')).data
    },

    async createProjectGroup(group) {
        return AXIOS.post('project-group/', group)
    },

    async deleteProjectGroup(projectGroup) {
        return AXIOS.delete('project-group/' + projectGroup.id + '/')
    },

    async updateProjectGroup(projectGroup) {
        return AXIOS.put('project-group/' + projectGroup.id + '/', projectGroup)
    },
    // TAG
    async getTags() {
        return (await AXIOS.get('tag/')).data
    },
    async createTag(name) {
        return AXIOS.post('tag/', {name})
    },
    // RESOURCE
    async createResource(resource) {
        return (await AXIOS.post('resource/', resource)).data
    },
    async getResources() {
        return (await AXIOS.get('resource/')).data
    },
    async updateResource(resource) {
        return await AXIOS.put('resource/' + resource.id + '/', resource)
    },
    async uploadImage(formData, filename) {
        return (await AXIOS.post("image/", formData, {
            headers: {
                'Content-Disposition': 'filename="' + filename + '"',
                'Content-Type': 'multipart/form-data'
            }
        })).data
    },

    async getJWT(code, provider) {
        try {
            const response = await AXIOS.post("/login/social/jwt-pair/", {
                provider,
                code
            })
            return response.data
        } catch (e) {
            console.log("Token conversion FAILED")
            console.log(e)
        }

    },

    // PERMISSIONS
    async getPermissionLevels() {
        return (await AXIOS.get('permission-level/')).data
    },

    async getPermissionRequests() {
        return (await  AXIOS.get('permission-request/')).data
    },

    async resolvePermissionRequest(id,expDate, approved, response) {
        const data = {
            expiration_date: expDate,
            approved: approved,
            response: response
        }
        return await  AXIOS.put('permission-request/'+id+'/resolve_request/',data)
    },

    async applyPermissionRequest(requestedLevel, reason) {
        const data = {
            requested_level: requestedLevel,
            reason: reason
        }
        return await AXIOS.put('permission-request/send_request/', data)
    },

    // RESERVATIONS
    async getReservations() {
        return (await AXIOS.get('reservation/')).data
    },

    async deleteReservation(id) {
        return (await AXIOS.delete('reservation/'+ id + '/'))
    },

    async resolveReservationRequest(id, approved) {
       return (await AXIOS.put('reservation/'+ id + '/resolve_reservation_request/', {approved}))
    },

    async takeUpResources(id, resources) {
        return (await AXIOS.put('reservation/'+ id + '/take_up_resources/', {resources}))
    },



    async createReservation(pickUpDate, returnDate, resources,approvalRequierd, project,provider) {
        const data = {
            pickup_date_time: pickUpDate,
            return_date_time: returnDate,
            resources: resources,
            approval_required: approvalRequierd,
            project,
            provider,
        }
        return (await AXIOS.put('reservation/create_reservation/',data)).data
    },
    async transmitReservation(id) {
        return (await  AXIOS.put('reservation/'+ id + '/transmit_reservation/'))
    },
    async getProviders() {
        return (await AXIOS.get('user/?role__in=ADMIN,PROVIDER')).data
    }

}
