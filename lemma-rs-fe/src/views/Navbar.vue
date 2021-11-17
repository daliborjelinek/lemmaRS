<template>
  <div>
    <v-app-bar
      elevation="10"
      color="#0000b657"
      dark
      style="right: 0; left: 0"
      app
    >
      <img height="80%" class="mr-1" src="../assets/lemma.png" />
      <v-spacer />
      <div :class="{'d-none': true, 'd-block': $vuetify.breakpoint.mdAndUp }">
        <v-btn @click="item.action" :key="item.text" v-for="item in items" text>
          {{ item.text }}
        </v-btn>
      </div>
      <div :class="{'d-none': $vuetify.breakpoint.mdAndUp }">
        <portal-target class="d-inline" name="responsive-buttons" />


      </div>
      <v-btn icon>
        <v-icon>mdi-help-circle-outline</v-icon>
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="$refs.userDialog.show()">
          {{$store.state.user.profile ? $store.state.user.profile.fullname : ''}}
          </v-list-item>
          <v-list-item @click="logout()" link>
           Odhlásit
          </v-list-item>
        </v-list>
      </v-menu>
      <v-app-bar-nav-icon class="d-md-none" @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" right temporary app>
      <v-list>
        <v-list-item-group>
          <template v-for="item in items">
            <v-list-item
              dense
              :key="item.text"
              :value="item"
              @click="item.action"
              active-class="primary--text text--accent-4"
            >
              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <user ref="userDialog"/>
  </div>
</template>
<script>
import axios from "axios";
import {AUTH_LOGOUT} from "@/store/actions/auth"
import User from "@/views/User";

export default {
  components: {User},
  data: function () {
    return {
      drawer: false,
      items: [
        {
          text: "Zdroje",
          action: () => this.$router.push({name: 'Resources'})
        },
        {
          text: "Projekty",
          action: () => this.$router.push({name: 'Projects'})
        },
        {
          text: "Rezervace",
          action: () => this.$router.push({name: 'Reservations'})
        },
        {
          text: "Oprávnění",
          action: () => this.$router.push({name: 'Permissions'})
        },
      ],
    };
  },
  methods: {
    logout(){
      this.$store.dispatch(AUTH_LOGOUT)
      this.$router.push({name: 'Login'});
    },
    changeDisplayRole(){

    }
  },
  created() {

  },
  destroyed() {},
};
</script>
