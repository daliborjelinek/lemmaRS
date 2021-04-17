<template>
  <v-app>
     <v-overlay z-index="0">
       
     </v-overlay>
    <navbar v-if="$route.name !== 'Login'" />
    <transition
      mode="out-in"
      name="fade"
    >
    <router-view/>
    </transition>
    <toaster/>
  </v-app>
</template>

<script>
import Navbar from "./views/Navbar"
import Toaster from "./components/Toaster"
import httpclient from '@/model/httpclient.js'
import { USER_REQUEST } from "@/store/actions/user";
export default {
  components:{
    Navbar,
    Toaster
  },
  created: function() {
    if (this.$store.getters.isAuthenticated) {
      this.$store.dispatch(USER_REQUEST);
    }
  }
};
</script>

<style lang="scss">
 @import "./styles/global.scss";

</style>