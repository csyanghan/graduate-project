import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userInfo: {},
  },
  mutations: {
    userLogin(state, payload) {
      state.userInfo = payload.userInfo;
    },
  },
  getters: {
    id: (state) => state.userInfo.id,
    username: (state) => state.userInfo.username,
  },
});
