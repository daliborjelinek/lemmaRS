<template lang="pug">
  div.fill-height
    v-card.fill-height.d-flex.flex-column(elevation='5' color='#1e1e1ee6' rounded='0')
      v-card-title Rezervace
        v-spacer
        v-btn( @click="sendReservation" :disabled='!reservationIsFilled || !reservationErrors.reservationIsValid' color='primary') odeslat
      v-card-text.flex-grow-1.d-flex.flex-column
        div
          //| {{$store.getters.hourCost}}
          v-alert.mb-1( v-if="$store.getters.approvalRequired" dense icon='mdi-alert' text='' type='warning') Vyžaduje schválení
          v-alert.mb-1( v-if="reservationErrors.timeConflicts.length > 0" dense icon='mdi-close-circle' text='' type='error') Konflikt s jinou rezervací
          v-alert.mb-1( v-if="reservationErrors.invalidProvider.length > 0" dense icon='mdi-close-circle' text='' type='error') Zdroje různých výdejářů
          v-form(ref="reservationForm")
            v-select(
              v-model="provider"
              prepend-icon="mdi-account-cog",
              @change="clearTimeAndDate",
              :items="providers",
              label="Výdejář",
              :item-text="(itm)=> itm.fullname"
              :item-value="(itm)=> itm.id" )
            v-dialog( v-model='showCalendar' width='290px')
              template(v-slot:activator='{ on, attrs }')
                v-text-field(v-model='dateRangeText'
                  label='Termín rezervace'
                  :rules="[(v) => !!v || 'Vyplňte termín rezervace']"
                  prepend-icon='mdi-calendar'
                  readonly v-bind='attrs'
                  v-on='on')
              v-date-picker(first-day-of-week='1' v-model='date' @change="setDate" :allowedDates="allowedDates", :min='$moment().format()' no-title range scrollable)
                v-spacer
                v-btn(text='' color='primary' @click='showCalendar = false')
                  | OK
            .d-flex
              v-autocomplete.pr-2(:items='providerAvailability.pickupTimes'
                :value="$store.state.reservation.startTime"
                color='white'
                no-data-text="Nejprve zvolte datum"
                @change="t => setTime(t,'start')"
                label='Začátek'
                auto-select-first
                prepend-icon='mdi-alarm-multiple')

              v-autocomplete(:items='providerAvailability.returnTimes'
                :value="$store.state.reservation.endTime"
                color='white'
                @change="t => setTime(t,'end')"
                no-data-text="Nejprve zvolte datum"
                auto-select-first
                label='Konec')
            v-autocomplete(:items='myProjects'
              :value="$store.state.reservation.project"
              color='white'
              @change="setProject"
              :item-value="(itm) => itm.id",
              :item-text="(itm) => itm.name"
              :rules="[(v) => !!v || 'Vyplňte projekt']"
              label='Projekt'
              prepend-icon='mdi-database-search'
              return-object)
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
              v-list-item-title(:class="resource.reservationIsPossible ?'' : 'error--text'") {{resource.name}}
            v-list-item-action
              v-btn(@click='removeResource(resource)' x-small='' icon='')
                v-icon(small='' color='grey lighten-1') mdi-delete

    project-editor-modal(ref="projectEditorModal")
</template>

<script>
import ApiSelect from "@/components/ApiSelect";
import ProjectEditorModal from "@/views/projects/ProjectEditorModal";
import API from '@/model/httpclient'
import {createHelpers} from "vuex-map-fields";
import Holidays from "date-holidays";

const {mapFields} = createHelpers({
  getterType: "getResField",
  mutationType: "updateResField",
});
const hd = new Holidays('CZ')
export default {
  components: {ApiSelect, ProjectEditorModal},
  data: () => ({
    providers: [],
    showCalendar: false
  }),
  async created() {
    const res = await API.getProviders()
    this.providers = res.filter(provider => provider.calendar_data.length)
  },
  computed: {
    date: {
      get() {
        return this.$store.state.reservation.dateRange

      },
      set(range) {
        const sorted = range.sort((a, b) => this.$moment(a) - this.$moment(b))
        this.$store.commit('setDate', sorted)
      },
    },
    providerAvailability() {
      const provider = this.providers.find((provider) => provider.id === this.provider)
      const startDate = this.$store.getters.startDate
      const endDate = this.$store.getters.endDate
      const availableDays = [...new Set(provider?.calendar_data.map(interval => interval.dow))]

      const pickupIntervals = startDate ? provider?.calendar_data.filter((rec) => rec.dow === this.$moment(startDate).day()) || [] : []
      const returnIntervals = endDate ? provider?.calendar_data.filter((rec) => rec.dow === this.$moment(endDate).day()) || [] : []

      const pickupTimes = []
      const returnTimes = []

      pickupIntervals.forEach((interval) => {
        let start = this.$moment(interval.start, 'HH:mm');
        let end = this.$moment(interval.end, 'HH:mm');
        while (end.isSameOrAfter(start)) {
          pickupTimes.push(start.format('HH:mm'));
          start.add(15, 'minutes');
        }
      })

      returnIntervals.forEach((interval) => {
        let start = this.$moment(interval.start, 'HH:mm');
        let end = this.$moment(interval.end, 'HH:mm');
        while (end.isSameOrAfter(start)) {
          returnTimes.push(start.format('HH:mm'));
          start.add(15, 'minutes');
        }
      })

      return {
        pickupIntervals,
        returnIntervals: this.$store.getters.endDate,
        availableDays,
        pickupTimes,
        returnTimes,
        holidays: provider?.holidays || []
      }

      while (start <= end) {
        result.push(start.format('HH:mm'));
        start.add(15, 'minutes');
      }
    },
    ...mapFields([
      'provider',
    ]),

    dateRangeText() {
      return this.$store.getters.startDate ? this.$store.getters.startDate + " ~ " + this.$store.getters.endDate : ''
    },
    selectedResources() {
      return this.$store.getters.selectedResourcesObj
    },
    myProjects() {
      return this.$store.getters.myProjects
    },
    reservationIsFilled() {
      return this.$store.getters.reservationIsFilled
    },

    reservationErrors() {
      return this.$store.getters.reservationErrors
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
      this.$store.commit('setDate', range)
      this.$store.commit('setTime', {time: null, type: 'start'})
      this.$store.commit('setTime', {time: null, type: 'end'})
    },
    setProject(val) {
      this.$store.commit('setProject', val.id)
    },
    clearTimeAndDate() {
      this.$store.commit('setDate', [])
      this.$store.commit('setTime', {time: null, type: 'start'})
      this.$store.commit('setTime', {time: null, type: 'end'})
    },
    allowedDates(val) {
      const providerHoliday = this.providerAvailability.holidays.find((hd) => this.$moment.range(this.$moment(hd.from), this.$moment(hd.to)).contains(this.$moment(val)))
      return this.providerAvailability.availableDays.includes(this.$moment(val).day()) && !(hd.isHoliday(val)) && !providerHoliday
    },
    async sendReservation() {
      if (!this.$refs.reservationForm.validate()) return;
      await this.$store.dispatch('sendReservation')
      this.$refs.reservationForm.resetValidation()
    },
    openNewProjectDialog() {
      this.$refs.projectEditorModal.openCreateDialog()
    }
  }
};
</script>
