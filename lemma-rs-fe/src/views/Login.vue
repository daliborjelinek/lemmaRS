<template>
  <v-main>
    <div id="login">
      <v-card>
        <v-card-text class="pt-4 text-center elevation-3">
          <div>
            <img height="50px" class="p-3" src="../assets/lemma.png" /><br />

            <p class="display-1">RS lemma</p>
            <div @click="loginMuni" class="munibtn" v-ripple></div>
          </div>
           <div v-if="mode === 'development'">
            <v-btn class="mt-2" @click="loginMock" >Mock login</v-btn>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </v-main>
</template>

><script>
import axios from 'axios'
import API from '@/model/httpclient'
import { USER_REQUEST } from "@/store/actions/user";
import {
  AUTH_REQUEST,
  AUTH_ERROR,
  AUTH_SUCCESS,
  AUTH_LOGOUT
} from "@/store/actions/auth";
export default {
  data(){
    return{
      auth_backend: 'muni',
    }
  },
  methods: {
    loginMuni() {
      const clientId='68a86438-6400-4b77-8a4a-d6b3a52ac6b6'
      const redirectUri= window.location.origin + '/auth/signinwin/main'
      this.auth_backend = 'muni';
      this.$store.commit(AUTH_REQUEST);
         const url =`https://oidc.muni.cz/oidc/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=openid profile email&response_type=code`
          window.open(url, "popup", "height=600,width=500");
    },
    loginMock() {
      const clientId='client-credentials-mock-client'
      const redirectUri= window.location.origin + '/auth/signinwin/main'
      this.auth_backend = 'mock';
      this.$store.commit(AUTH_REQUEST);
      const url =`http://localhost:4011/connect/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=openid profile email&response_type=code`

      window.open(url, "popup", "height=600,width=500");
    },
    async authCallback(event) {
      if ((event.origin !== window.location.origin) || (event.source.name !== 'popup')) return;
      console.log(event.data)
      try{
        await this.$store.dispatch(AUTH_REQUEST,{code: event.data.code, backend: this.auth_backend})
        this.$router.push('/');
      }catch (e){
        this.$store.dispatch('notify',{type:'error', text: 'Přihlášení selhalo'})
      }

    },
  },
  created() {
    window.addEventListener("message", this.authCallback, false);
  },
  destroyed() {
      window.removeEventListener("message", this.authCallback);
  },
  computed:{
    mode: () => process.env.NODE_ENV
  }
};
</script>
<style scoped>
#login {
  display: grid;
  place-items: center;
  height: 100%;
}
.munibtn {
  background-image: url("~@/assets/dark_cs-min.png");
  background-size: contain;
  width: 260px;
  height: 46px;
  cursor: pointer;
}
</style>
