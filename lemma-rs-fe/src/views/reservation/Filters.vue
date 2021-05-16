<template lang="pug">
  v-card.flex-grow-1.d-flex.flex-column.fill-height(elevation='5' color='#1e1e1ee6' rounded='0')
    v-card-title
      | Filtry
      v-spacer
      v-btn-toggle(mandatory='' v-model='filtersData.displayStyle')
        v-btn(value='cards' small='')
          v-icon mdi-apps
        v-btn(value='table' small='')
          v-icon mdi-format-list-bulleted
      //
        <v-btn icon >
        <v-icon small class="mr-1">fas fa-sort-amount-down</v-icon>
        </v-btn>
    v-card-text
      portal-target(name='add-resource-btn')
      v-text-field.ma-0.pa-0(v-debounce:300ms='search' placeholder='Hledat' persistent-hint='' :hint="'Zobrazeno '+ $store.getters.filteredResourcesCount + ' výsledků'" append-icon='mdi-magnify')
      .d-flex.align-center.mt-2
        v-switch.mt-0.py-0.d-flex.align-center(hide-details='' v-model="alreadyReserved" label='Rezervované v termínu')
        v-spacer
        v-btn(small='' icon='')
          v-icon(small='') mdi-information-outline
      .d-flex.align-center.mt-2
        v-switch.mt-0.py-0.d-flex.align-center(hide-details='' v-model="disallowed" label='Bez oprávnění')
        v-spacer
        v-btn(small='' icon='')
          v-icon(small='') mdi-information-outline
      .d-flex.align-center.mt-2
        v-switch.mt-0.py-0.d-flex.align-center(hide-details='' v-model="inactive" label='Neodstupné')
        v-spacer
        v-btn(small='' icon='')
          v-icon(small='') mdi-information-outline
      v-divider.mt-2
    v-list-item-group.flex-grow-1(@change='filterTagChanged' style='height: 200px; overflow-y: auto')
      template(v-for='(item, i) in items')
        v-list-item(dense='' :key='`item-${i}`' :value='item')
          v-list-item-icon
            v-icon {{ item.icon }}
          v-list-item-content
            v-list-item-title(v-text='item.name')

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
        'inactive',
        'disallowed',
        'alreadyReserved'

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
