<template>
  <v-main class="d-flex">
    <div id="filter-sidebar" :class="{ show: $vuetify.breakpoint.mdAndUp }">

      <reservation-sidebar />
    </div>
    <div
      id="reservation-sidebar"
      :class="{ show: $vuetify.breakpoint.mdAndUp }"
    >
      <filters :filtersData="filtersData" />
    </div>
    <div
      id="reservation-items"
      :class="{ 'show-sidebars': $vuetify.breakpoint.mdAndUp }"
    >
      <resources :displayStyle="filtersData.displayStyle" />
    </div>
    <v-navigation-drawer floating v-model="drawer" temporary app>

      <reservation-sidebar v-if="drawerContent === 'reservation'" />
      <filters :filtersData="filtersData" v-if="drawerContent === 'filters'" />
    </v-navigation-drawer>
    <portal to="responsive-buttons">
      <v-btn @click="drawer=true; drawerContent='reservation'" icon class="ml-1">
        <v-icon>mdi-calendar-edit</v-icon>
        <v-badge
            v-if="$store.state.reservation.selectedResources.length"
            color="purple"
            :content="$store.state.reservation.selectedResources.length"

        >

        </v-badge>
      </v-btn>
      <v-btn @click="drawer=true; drawerContent='filters'" icon class="ml-1">
        <v-icon>mdi-filter</v-icon>
      </v-btn>
    </portal>
  </v-main>
</template>

<style>
#filter-sidebar,
#reservation-sidebar {
  transition: transform ease 0.2s;
   position: fixed;
  width: 280px;
  height: 100%;
  padding-bottom: 64px;
}

#filter-sidebar.show,
#reservation-sidebar.show {
  transform: translateX(0);
}

#filter-sidebar {
  transform: translateX(-100%);
}

#reservation-items {
  display: flex;
  flex-direction: column;
  height: 100%;
}
#reservation-items.show-sidebars {
  padding: 0 280px;
}
#reservation-sidebar {
  right: 0;
  transform: translateX(100%);
}

</style>

<script>
import Filters from "./reservation/Filters";
import ReservationSidebar from "./reservation/ReservationSidebar";
import Resources from "./reservation/Resources"
export default {
  data: () => ({
    drawer: false,
    drawerContent: 'reservation',
    filtersData: {
          displayStyle: 'cards',
          searchString: '',
        },

  }),
  components: { Filters, ReservationSidebar, Resources },
};
</script>
