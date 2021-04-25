
import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT
} from "../actions/auth";
import { USER_REQUEST } from "../actions/user";
import API from "@/model/httpclient.js"


const state = {
  token: localStorage.getItem("user-token") || "",
  refreshToken: localStorage.getItem("refresh-token") || "",
  status: "",
  hasLoadedOnce: false
};

const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status
};

const actions = {
  [AUTH_REQUEST]: async ({ commit, dispatch }, {token, backend}) => {

    const tokens = await API.convertToken(token,backend)
    commit(AUTH_SUCCESS,tokens)
    console.log(tokens.accessToken)
    localStorage.setItem('user-token', tokens.accessToken)
    localStorage.setItem('refresh-token', tokens.refreshToken)
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
    state.token = resp.accessToken;
    state.refreshToken = resp.refreshToken
    state.hasLoadedOnce = true;
  },
  [AUTH_ERROR]: state => {
    state.status = "error";
    state.hasLoadedOnce = true;
  },
  [AUTH_LOGOUT]: state => {
    state.token = "";
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
