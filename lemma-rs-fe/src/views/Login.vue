<template>
  <v-main>
    <div id="login">
      <v-card>
        <v-card-text class="pt-4 text-center elevation-3">
          <div>
            <img height="50px" class="p-3" src="../assets/lemma.png" /><br />

            <p class="display-1">RS lemma</p>
            <div @click="login()" class="munibtn" v-ripple></div>
          </div>
           <div>
           
            <v-btn @click="login2()" >Mock login</v-btn>
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
  methods: {
    login() {
      this.$store.commit(AUTH_REQUEST);
         const url =
         "https://oidc.muni.cz/oidc/authorize?client_id=68a86438-6400-4b77-8a4a-d6b3a52ac6b6&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&response_mode=form_post";
        //"http://localhost:4011/connect/authorize?client_id=implicit-mock-client&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&nonce=cppd09c80j9"
         
         const newwindow = window.open(url, "popup", "height=600,width=500");
    },
    login2() {
      this.$store.commit(AUTH_REQUEST);
         const url =
        // "https://oidc.muni.cz/oidc/authorize?client_id=68a86438-6400-4b77-8a4a-d6b3a52ac6b6&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&response_mode=form_post";
        "http://localhost:4011/connect/authorize?client_id=implicit-mock-client&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&nonce=cppd09c80j9"
         
         const newwindow = window.open(url, "popup", "height=600,width=500");
    },
    async authCallback(event) {      
      if ((event.origin !== 'http://localhost:8080') || (event.source.name !== 'popup')) return;     
      await this.$store.dispatch(AUTH_REQUEST,event.data.token)
      this.$router.push('/');
    },
  },
  created() {
    window.addEventListener("message", this.authCallback, false);
  },
  destroyed() {
      window.removeEventListener("message", this.authCallback);
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