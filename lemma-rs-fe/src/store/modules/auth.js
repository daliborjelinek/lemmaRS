
import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT
} from "../actions/auth";
import { USER_REQUEST } from "../actions/user";
import API from "@/model/httpclient.js"
import router from "@/router";


const state = {
  tokenProvided: !!localStorage.getItem("user-token"),
  status: "",
  hasLoadedOnce: false
};

const getters = {
  isAuthenticated: state => state.tokenProvided,
  authStatus: state => state.status
};

const actions = {
  [AUTH_REQUEST]: async ({ commit, dispatch }, {code, backend}) => {
    const tokens = await API.getJWT(code, backend)
    commit(AUTH_SUCCESS,tokens)
    localStorage.setItem('user-token', tokens.token)
    localStorage.setItem('refresh-token', tokens.refresh)
    await dispatch(USER_REQUEST)
  },
  [AUTH_LOGOUT]: ({ commit }) => {
      commit(AUTH_LOGOUT);
      localStorage.removeItem("user-token");
      localStorage.removeItem("refresh-token");
  }
};

const mutations = {
  [AUTH_REQUEST]: state => {
    state.status = "loading";
  },
  [AUTH_SUCCESS]: (state, resp) => {
    state.status = "success";
    state.tokenProvided = true;
  },
  [AUTH_ERROR]: state => {
    state.status = "error";
  },
  [AUTH_LOGOUT]: state => {
    state.tokenProvided = false;
    router.push('Login')
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
