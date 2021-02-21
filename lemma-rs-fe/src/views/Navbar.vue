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
      <div class="d-none d-md-block">
        <v-btn :key="item.text" v-for="item in items" text>
          {{ item.text }}
        </v-btn>
      </div>
      <div class="d-md-none">
        <portal-target class="d-inline" name="responsive-buttons" />

        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </div>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon>fas fa-user</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="login()" link>
            <img width="250px" src="@/assets/dark_cs-min.png" />
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" right temporary app>
      <v-list>
        <v-list-item-group>
          <template v-for="item in items">
            <v-list-item
              dense
              :key="item.text"
              :value="item"
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
  </div>
</template>
<script>
import axios from "axios";
export default {
  data: function () {
    return {
      drawer: false,
      items: [
        {
          text: "Rezervace",
        },
        {
          text: "Registrace",
        },
        {
          text: "Zdroje",
        },
        {
          text: "Projekty",
        },
        {
          text: "Osoby",
        },
      ],
    };
  },
  methods: {
    login() {
      //this.$oidc.signIn()
      const url =
        "https://oidc.muni.cz/oidc/authorize?client_id=68a86438-6400-4b77-8a4a-d6b3a52ac6b6&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&response_mode=form_post&nonce=oi139wu8tqj";
      const newwindow = window.open(url, "name", "height=600,width=500");
    },
  },
  created() {
    window.addEventListener(
      "message",
      (event) => {
        if (event.origin !== process.env.BASE_URL) return;
        console.log(event);
        event.data.token;
        // Do we trust the sender of this message?  (might be
        // different from what we originally opened, for example).
        axios.get("http://localhost:8000/auth/convert-token", {
          params: {
            ID: 12345,
          },
        });

        //  alert('HURAAAAAAAAAAA')
        // event.source is popup
        // event.data is "hi there yourself!  the secret response is: rheeeeet!"
      },
      false
    );
  },
  destroyed() {},
};
</script>