<template>
  <v-app id="inspire">
     <v-overlay z-index="0">
       
     </v-overlay>
    <navbar v-if="$route.name !== 'Login'" />

    <router-view/>

  </v-app>
</template>

<script>
import Navbar from "./views/Navbar"
export default {
  components:{
    Navbar
  },
  created(){
    
  }
};
</script>

<style lang="scss">
 @import "./styles/global.scss";

</style>