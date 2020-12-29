<template>
  <v-app id="inspire">
    
    <navbar />

    <router-view/>

  </v-app>
</template>

<script>
import Navbar from "./views/Navbar"
export default {
  components:{
    Navbar
  }
};
</script>

<style lang="scss">
 @import "./styles/global.scss";

</style>