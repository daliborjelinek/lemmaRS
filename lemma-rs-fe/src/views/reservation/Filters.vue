<template>
  <v-card class="flex-grow-1 d-flex flex-column fill-height"  elevation="5" color="#1e1e1ee6" rounded="0">
    <v-card-title>
      Filtry <v-spacer />
       <v-btn-toggle mandatory v-model="filtersData.displayStyle">
        <v-btn value="cards" small>
          <v-icon >mdi-apps</v-icon>
        </v-btn>

        <v-btn value="table"  small>
          <v-icon >mdi-format-list-bulleted</v-icon>
        </v-btn>
      </v-btn-toggle>
      <!-- <v-btn icon >
        <v-icon small class="mr-1">fas fa-sort-amount-down</v-icon>
      </v-btn> -->
    </v-card-title>

    <v-card-text>
       <portal-target name="add-resource-btn" />
      <v-text-field
          v-debounce:300ms="search"
        placeholder="Hledat"
        class="ma-0 pa-0"
        persistent-hint
        :hint="'Zobrazeno '+ $store.getters.filteredResourcesCount + ' výsledků'"
        append-icon="mdi-magnify"
      ></v-text-field>

      <div class="d-flex align-center mt-2">
        <v-switch
          class="mt-0 py-0 d-flex align-center"
          hide-details
          :input-value="true"
          label="Rezervované v termínu"
        ></v-switch>
        <v-spacer /><v-btn small icon
          ><v-icon small>mdi-information-outline</v-icon></v-btn
        >
      </div>
      <div class="d-flex align-center mt-2">
        <v-switch
          class="mt-0 py-0 d-flex align-center"
          hide-details
          :input-value="false"
          label="Bez oprávnění"
        ></v-switch>
        <v-spacer /><v-btn small icon
          ><v-icon small>mdi-information-outline</v-icon></v-btn
        >
      </div>
      <div class="d-flex align-center mt-2">
        <v-switch
          class="mt-0 py-0 d-flex align-center"
          hide-details
          :input-value="false"
          label="Neodstupné"
        ></v-switch>
        <v-spacer /><v-btn small icon
          ><v-icon small>mdi-information-outline</v-icon></v-btn
        >
      </div>
      <v-divider class="mt-2"></v-divider>
    </v-card-text>

    <v-list-item-group
        class="flex-grow-1"
        @change="filterTagChanged"
        style="height: 200px; overflow-y: auto">
      <template v-for="(item, i) in items">
        <v-list-item dense :key="`item-${i}`" :value="item">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="item.name"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list-item-group>
  </v-card>
</template>

<script>
import {createHelpers} from "vuex-map-fields";

const { mapFields } = createHelpers({
  getterType: "getResField",
  mutationType: "updateResField",
});
export default {
  props: ['filtersData'],
  computed:{
    ...mapFields([

    ]),
    filters(){
      return this.$store.state.reservation.search
    }
  },
  methods:{
    search(e){
      this.$store.commit('setSearch',e)
      console.log(e)
    },
    filterTagChanged(tag){

      this.$store.commit('setTagFilter',tag?.value)
    }
  },
  data: function () {
    return {
      toggl: 'cards',
      items: [
        {
          value: 1,
          name: "AUDIO",
          icon: "mdi-microphone-variant",
        },
        {
          value: 2,
          name: "VIDEO",
          icon: "mdi-video-vintage",
        },
        {
          value: 3,
          name: "OBJEKTIVY",
          icon: "mdi-camera-iris",
        },
        {
          value: 4,
          name: "STABILIZACE",
          icon: "mdi-video-stabilization",
        },
        {
          value: 5,
          name: "SVĚTLA",
          icon: "mdi-spotlight-beam",
        },
        {
          value: 6,
          name: "PŘÍSLUŠENSTVÍ",
          icon: "mdi-battery-charging-high",
        }
      ],
    };
  },
};
</script>
