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

        <v-menu offset-y>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" icon>
              <v-icon>fas fa-user</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link>
              <v-list-item-title v-text="'Log out'"></v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <div class="d-md-none">
        <portal-target class="d-inline" name="responsive-buttons" />

        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      </div>
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
};
</script>