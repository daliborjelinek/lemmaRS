<template lang="pug">
  div.fill-height
    v-card.fill-height.d-flex.flex-column(elevation='5' color='#1e1e1ee6' rounded='0')
      v-card-title Rezervace
        v-spacer
        v-btn( @click="sendReservation" :disabled='!reservationIsValid' color='primary') odeslat
      v-card-text.flex-grow-1.d-flex.flex-column
        div
          | {{$store.getters.hourCost}} {{$store.getters.approvalRequired}}
          v-alert.mb-0( v-if="$store.getters.approvalRequired" dense icon='mdi-alert' text='' type='warning') Vyžaduje schválení
          v-form(ref="reservationForm")
            api-select(
              v-model="provider"
              prepend-icon="mdi-account-cog",
              query="user/?role__in=ADMIN,PROVIDER"
              :default-index="1",
              label="Výdejář",
              :item-value="(itm)=> itm.id" ,
              :item-text="(itm)=> itm.fullname")
            v-dialog( v-model='showCalendar' width='290px')
              template(v-slot:activator='{ on, attrs }')
                v-text-field(v-model='dateRangeText' label='Termín rezervace' :rules="[(v) => !!v || 'Vyplňte termín rezervace']" prepend-icon='mdi-calendar' readonly v-bind='attrs' v-on='on')
              v-date-picker(first-day-of-week='1' v-model='date' @change="setDate" :allowedDates="allowedDates", :min='$moment().format()' no-title range scrollable)
                v-spacer
                v-btn(text='' color='primary' @click='showCalendar = false')
                  | OK
            .d-flex
              timepicker.pr-2(icon='true' label='Začatek' @change="t => setTime(t,'start')" :value="$store.state.reservation.startTime")
              timepicker.mb-2(label='Konec' @change="t => setTime(t,'end')" :value="$store.state.reservation.endTime")
            v-autocomplete(:items='myProjects'
              :value="$store.state.reservation.project"
              color='white'
              @change="setProject"
              :item-value="(itm) => itm.id",
              :item-text="(itm) => itm.name"
              :rules="[(v) => !!v || 'Vyplňte projekt']"
              label='Projekt'
              prepend-icon='mdi-database-search'
              return-object='')
              template(v-slot:append-item)
                v-divider
                v-list-item(link @click="openNewProjectDialog")
                  v-list-item-avatar.mr-0
                    v-icon(small) mdi-plus-circle
                  v-list-item-content
                    v-list-item-title Nový projekt

        v-divider.mt-3
        v-list-item-group.flex-grow-1(style='height: 200px; overflow-y: auto')
          v-list-item(dense='' v-for='(resource, i) in selectedResources' :title="resource.name" :key='resource.id')
            v-list-item-content
              v-list-item-title {{resource.name}}
            v-list-item-action
              v-btn(@click='removeResource(resource)' x-small='' icon='')
                v-icon(small='' color='grey lighten-1') mdi-delete

    project-editor-modal(ref="projectEditorModal")
</template>

<script>
import Timepicker from "@/components/Timepicker";
import ApiSelect from "@/components/ApiSelect";
import ProjectEditorModal from "@/views/Projects/ProjectEditorModal";
import {createHelpers} from "vuex-map-fields";
const { mapFields } = createHelpers({
  getterType: "getResField",
  mutationType: "updateResField",
});

export default {
  components: {ApiSelect, Timepicker,ProjectEditorModal},
  data: () => ({
    date: [],
    showCalendar: false
  }),

  computed: {
    ...mapFields([
      'provider',
    ]),
    dateRangeText(){
      return this.$store.state.reservation.startDate ?
      this.$store.state.reservation.startDate + " ~ " + this.$store.state.reservation.endDate: null
    },
    selectedResources() {
      return this.$store.state.reservation.selectedResources
    },
    myProjects() {
      return this.$store.getters.myProjects
    },
    reservationIsValid() {
      return this.$store.getters.hourCost > 0
    }

  },
  methods: {
    removeResource(res) {
      this.$store.commit('removeSelectedItem', res)
    },
    setTime(time, type) {
      this.$store.commit('setTime', {time, type})
    },
    setDate(range) {
      console.log(range)
      if (range.length === 2) {
        this.$store.commit('setDate', {start: range[0], end: range[1]})
      }
    },
    setProject(val){
      this.$store.commit('setProject',val.id)
    },
    allowedDates(val) {
      return ![6, 0].includes(this.$moment(val).day())
    },
    async sendReservation(){
        if(!this.$refs.reservationForm.validate()) return;
        await this.$store.dispatch('sendReservation')
        this.$refs.reservationForm.resetValidation()
    },
    openNewProjectDialog(){
      this.$refs.projectEditorModal.openCreateDialog()
    }
  }
};
</script>
