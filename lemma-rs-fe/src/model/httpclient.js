import axios from 'axios'
import store from '@/store'
import router from '@/router'
import {
  AUTH_LOGOUT
} from "@/store/actions/auth";



export const AXIOS = axios.create({
  baseURL: "http://localhost:8000",
  headers: {}
})

// Add a request interceptor
AXIOS.interceptors.request.use(
  config => {
    const token = localStorage.getItem('user-token');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    // config.headers['Content-Type'] = 'application/json';
    return config;
  },
  error => {
    Promise.reject(error)
  });



//Add a response interceptor


AXIOS.interceptors.response.use(undefined, (err) => {
  return new Promise(function (resolve, reject) {

    if (err.response.status === 401) {

      // if you ever get an unauthorized, logout the user
      store.dispatch(AUTH_LOGOUT)
      router.push({ name: 'Login' })
    }
    throw err;
  });
});

export default {
  async getUsers(){
    return (await  AXIOS.get('user/')).data
  },
  // USER
  async getCurentUser() {
    return (await AXIOS.get('user/current')).data
  },
  async putUser(user) {
    return AXIOS.put('user/' + user.id + '/', user)
  },
  // PROJECT
  async getProjects() {
    return ( await AXIOS.get('project/')).data
  },
  async createProject(project) {
    return (await AXIOS.post('project/',project)).data
  },
  async updateProject(project) {
    return AXIOS.put('project/' + project.id + '/', project)
  },
  async addProjectMember(projectId,memberId) {
    return AXIOS.put('project/'+ projectId + '/add_member/?userId='+ memberId)
  },
  async removeProjectMember(projectId, memberId) {
    return AXIOS.delete('project/'+ projectId + '/remove_member/?userId='+ memberId)
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

  async convertToken(token) {
    try {
      const response = await AXIOS.post("auth/convert-token", {
        grant_type: 'convert_token',
        token,
        backend: 'mock',
        client_id: 'Ke7ZcPRrR6n0EMJ9r0cScpLCmxzFgU9IFWOi1FSk',
        client_secret: '9mxyEy1dRxNN4RnhySpCULusSZpEY0EFeuwVMrzFgoTz3e34rr4ew5dyijLyOAQc6E778GIBU8pHpixwk0AmrZnJnlRtf6jY04pQ5dhd7SfLqo82SMnVxv9jSdUHGpSA'
      })

      return {
        accessToken: response.data.access_token,
        refreshToken: response.data.refresh_token
      }
    } catch (e) {
      console.log("Token conversion FAILED")
      console.log(e)
    }

  },
}
