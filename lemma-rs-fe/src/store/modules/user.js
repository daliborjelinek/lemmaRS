import { USER_REQUEST, USER_ERROR, USER_SUCCESS, USER_UPDATE, USER_SET_ROLE } from "../actions/user";
import API from "@/model/httpclient.js"
import Vue from "vue";
import { AUTH_LOGOUT } from "../actions/auth";
import { createHelpers } from 'vuex-map-fields';

const { getUserField, updateUserField } = createHelpers({
  getterType: 'getUserField',
  mutationType: 'updateUserField',
});

const state = { status: "",
                profile: {},
                tempRole: "" 
              };

const getters = {
  getProfile: state => state.profile,
  getRole: state => state.profile.role,
  isProfileLoaded: state => !!state.profile.fullname,
  getUserField
};

const actions = {
  [USER_REQUEST]: async ({ commit, dispatch }) => {
    commit(USER_REQUEST);
    try{
      const user = await API.getCurentUser()
      console.log(user)
    commit(USER_SUCCESS, user);
    } catch(e) {
      commit(USER_ERROR);
      // if resp is unauthorized, logout, to
      dispatch(AUTH_LOGOUT);
    }
  },
  [USER_UPDATE]: async ({ commit, dispatch }) => {
    console.log('tadyyyyyy')
    try{
      const response = await API.putUser(state.profile)
      dispatch('notify',{type:'success', text: 'Uživatel uložen' })
      console.log(response)
    } catch(e) {
      commit(USER_ERROR);
      dispatch('notify',{type:'error', text: 'Ukládání uživatele se nezdařilo'})
      console.log(e)

    }
  }
};

const mutations = {
  updateUserField,
  [USER_REQUEST]: state => {
    state.status = "loading";
  },
  [USER_SUCCESS]: (state, user) => {
    state.status = "success";
    Vue.set(state, "profile", user);
  },
  [USER_ERROR]: state => {
    state.status = "error";
  },
  [AUTH_LOGOUT]: state => {
    state.profile = {};
  },
  [USER_SET_ROLE]: (state,role) => {
    state.profile.role = role;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
