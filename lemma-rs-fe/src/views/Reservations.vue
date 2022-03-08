<template lang="pug">
  v-main
    v-container
      v-card
        v-tabs(v-model="tab")
          v-tab(v-if="userRole === 'ADMIN'", href="#pending_approval") Ke schválení
          v-tab(v-if="userRole !== 'COMMON'", href="#toTransmit") K vydání
          v-tab(v-if="userRole !== 'COMMON'", href="#toTakeUp") K převzetí
          v-tab(href="#my")  Moje rezervace
          v-tab(href="#planned")  Plánované
          v-tab(href="#all" v-if="userRole !== 'COMMON'", @change="tab='all'")  Vše

      v-data-table.elevation-1.pointer-rows(:headers='headers'
        id="reservationTable"
        :items='filteredItems'
        fixed-header,
        :search='search'
        @click:row="openReservationDialog"
        :footer-props="{'items-per-page-options': [10, 50, 100]}"
        :items-per-page='50')
        template(v-slot:top)
          v-toolbar(flat)
            v-text-field(style='max-width: 300px'
              v-model='search'
              append-icon='mdi-magnify'
              label='Hledat'
              single-line
              hide-details)
            v-spacer
            v-btn(color='primary' @click.stop='openCalendar' text)
              v-icon(left) mdi-calendar
              | Kalendář
        template(v-slot:item.applicant='{ item }') {{item.applicant.fullname}}
        template(v-slot:item.created_at='{ item }') {{$moment(item.created_at).locale("cs").format('LLL')}}
        template(v-slot:item.pickup_date_time='{ item }') {{$moment(item.pickup_date_time).locale("cs").format('LLL')}}
        template(v-slot:item.return_date_time='{ item }') {{$moment(item.return_date_time).locale("cs").format('LLL')  + ' (' + ($moment(item.return_date_time).diff($moment(item.pickup_date_time), "days")+1) + 'd)'}}
        template(v-slot:item.approved='{ item }')
          v-icon(v-if="item.approved === null") mdi-help-box
          v-icon(v-else-if="item.approved === false" color='error') mdi-close-box
          v-icon(v-else color='success') mdi-checkbox-marked
        template(v-slot:item.picked_up='{ item }')
          v-icon(v-if="!item.picked_up") mdi-checkbox-blank-outline
          v-icon(v-else color='success') mdi-checkbox-marked
        template(v-slot:item.fully_returned='{ item }')
          v-icon(v-if="item.fully_returned" color="success") mdi-checkbox-marked
          v-icon(v-else-if="item.picked_up && !item.fully_returned && item.returnDatePassed" color='error') mdi-close-box
          v-icon(v-else) mdi-checkbox-blank-outline

        template(v-slot:item.actions='{ item }')
          span(style="white-space: nowrap")
            v-btn.mr-1(v-if="userRole !== 'COMMON'" small color="primary" @click.stop="transmitReservation(item)" :disabled='!item.isTransmittable')
              v-icon(left) mdi-handshake
              | vydat
            v-btn.mr-1( icon color="warning" @click.stop="deleteReservation(item)" :disabled="item.picked_up === true || item.returnDatePassed")
              v-icon mdi-delete-circle
            v-btn(icon v-if="userRole === 'ADMIN'" @click.stop="resolveReservationRequest(item,true)" color="success" :disabled="item.approved !== null || item.returnDatePassed" title="Schválit")
              v-icon mdi-check-decagram
            v-btn(icon v-if="userRole === 'ADMIN'" color="error" @click.stop="resolveReservationRequest(item, false)" :disabled="item.approved !== null || item.returnDatePassed" title="Zamítnout")
              v-icon mdi-close-octagon-outline
      pdf-creator( ref="pdfCreator" :reservation="selectedReservation", :resources2="formatedResources")
      v-dialog(v-model="calendarDialog" max-width="900")
        v-card
          v-toolbar(color="primary", dark)
            | Rezervace
            v-spacer
            v-btn.ma-2(
              icon,
              @click="$refs.calendar.prev() "
            )
              v-icon mdi-chevron-left
            span.text-center(style='width:125px')
              span.text-button {{ calendarMonth }}
            v-btn.ma-2(icon, @click="$refs.calendar.next()")
              v-icon mdi-chevron-right
            v-btn(icon, @click="calendarDialog = false")
              v-icon mdi-close
          v-sheet.pa-2()
            v-calendar(
              v-model="calendarModel",
              :weekdays=[1, 2, 3, 4, 5, 6, 0],
              ref="calendar",
              color="primary",
              :events="calendarEvents",
              @click:event="evt => openReservationDialog(evt.event.reservation)"
              type="month"
            )
      v-dialog(max-width="900px" v-model="reservationDialog")
        v-toolbar(color="primary")
          | {{selectedReservation ? selectedReservation.applicant.fullname + ' - ' + selectedReservation.project : '' }}
          v-spacer
          v-btn(icon, @click="reservationDialog = false")
            v-icon mdi-close
        v-sheet.pa-2(v-if="reservationDialog===true")
          v-data-table(v-model='selectedResources' :items='formatedResources',  fixed-header style="height:calc(90vh - 132px)" height="calc(100% - 64px)" disable-pagination :hide-default-footer="true" :headers='resourcesHeaders' :show-select="userRole !== 'COMMON'")
            template(v-slot:item.comment='{ item }')
              v-text-field.my-1(v-model="item.comment" v-if="selectedResources.indexOf(item)!==-1 && userRole !== 'COMMON' && selectedReservation.picked_up" solo hide-details label="Popis defektů...")
              span(v-else)
                | {{item.comment}}
            template(v-slot:top)
              v-toolbar(flat v-if="userRole !== 'COMMON'")
                v-btn(color='primary' :disabled='!selectedResources.length || !selectedReservation.picked_up' @click.stop='takeUpResources')
                  v-icon(left) mdi-handshake
                  | převzít
                v-btn.ml-2(color='primary' @click.stop='print')
                  v-icon(left) mdi-printer
                  | tisk
                v-btn.ml-2(color='primary' @click.stop='copy')
                  v-icon(left) mdi-content-copy
                  | rezervovat znovu


</template>

<script>
import API from "@/model/httpclient";
import PdfCreator from "@/components/PdfCreator";

export default {
  name: "Reservations",
  components: {PdfCreator},
  data: function () {
    return {
      calendarDialog: false,
      reservationDialog: false,
      selectedReservation: null,
      selectedResources: [],
      calendarModel: new Date(),
      // newRequest: emptyRequest(),
      // newResolve: emptyResolve(true),
      tab: 'pending',
      // createDialog: false,
      // resolveDialog: false,
      search: '',
      reservations: [],
      loading: true,
      resourcesHeaders: [
        {text: 'Zdroj', value: 'resource_str'},
        {text: 'Vyzvednuto', value: 'real_pickup_date'},
        {text: 'Vráceno', value: 'real_return_date'},
        {text: 'Komentář', value: 'comment'},
        // {text: 'Akce', value: 'actions'}

      ]

    }
  },
  async created() {

    this.reservations = await API.getReservations()
    this.loading = false

  },
  computed: {
    calendarEvents() {
      return this.reservations.map(res => {
        return {
          start: new Date(res.pickup_date_time),
          end: new Date(res.return_date_time),
          name: res.applicant.fullname + ' - ' + res.project,
          timed: true,
          color: this.$randomColor({seed: res.project, luminosity: 'dark'}),
          reservation: res
        }
      })
    },
    calendarMonth() {
      return new Date(this.calendarModel).toLocaleString("cs-CZ", {month: "long", year: 'numeric'});
    },
    filteredItems() {
      return this.reservations.map(itm => {
        return {
          ...itm,
          isTransmittable:
          //(new Date(itm.pickup_date_time) <= new Date()) &&
              (new Date(itm.return_date_time) > new Date()) &&
              itm.approved &&
              !itm.picked_up,
          returnDatePassed: new Date(itm.return_date_time) < new Date(),
          isTransmittableString: "rezarevace začala " + (new Date(itm.pickup_date_time) <= new Date()) + '\n' +
              " rezarvace neskončila: " + (new Date(itm.return_date_time) > new Date()) +
              ' rezervace je schvalena:  ' + itm.approved + '\n' +
              ' rezervace není vyzvednuta ' + !itm.picked_up
        }
      }).filter(itm => {
        if (this.tab === 'my') return itm.applicant.id === this.$store.getters.getProfile.id
        if (this.tab === 'pending_approval') return itm.approved === null && !itm.returnDatePassed
        if (this.tab === 'toTransmit') return itm.isTransmittable
        if (this.tab === 'planned') return !itm.picked_up && (new Date(itm.return_date_time) > new Date())
        if (this.tab === 'toTakeUp') return (itm.picked_up && !itm.fully_returned)
        return true
      })
    },
    formatedResources() {
      return this.selectedReservation?.resources.map(res => {
        return {
          ...res,
          real_pickup_date: res.real_pickup_date ? this.$moment(res.real_pickup_date).locale("cs").format('LLL') : 'nevyzvednuto',
          real_return_date: res.real_return_date ? this.$moment(res.real_return_date).locale("cs").format('LLL') : 'nevráceno',
          isSelectable: !res.real_return_date
        }
      })
    },
    userRole() {
      return this.$store.getters.getDisplayRole
    },
    headers() {
      let headers = [
        {text: "Žadatel", value: "applicant"},
        {text: "Projekt", value: "project"},
        {text: "Vytvořeno", value: "created_at"},
        {text: "Od", value: "pickup_date_time"},
        {text: "Do", value: "return_date_time"},
        {text: "Schváleno", value: "approved"},
        {text: "Vyzvednuto", value: "picked_up"},
        {text: "Vráceno", value: "fully_returned"},
        {text: "Akce", value: "actions", sortable: false},
      ]
      if (this.$store.getters.getDisplayRole === 'COMMON' || this.tab === 'my') headers = headers.filter(h => h.value !== 'applicant')
      return headers
    },
  },
  methods: {
    openReservationDialog(reservation) {
      this.selectedReservation = reservation
      this.selectedResources = []
      this.reservationDialog = true
    },
    async transmitReservation(item) {
      if(!confirm("Potvrďte prosím předání " + item.resources.length + " zdrojů uživateli " + item.applicant.fullname )) return
      await API.transmitReservation(item.id)
      this.reservations = await API.getReservations()
    },
    async deleteReservation(item) {
      if (confirm("Opravdu chcete zrušit tuto rezerevaci?"))
        await API.deleteReservation(item.id)
      this.reservations = await API.getReservations()
    },
    async resolveReservationRequest(item, approved) {
      await API.resolveReservationRequest(item.id, approved)
      this.reservations = await API.getReservations()
    },
    async takeUpResources() {
      if(!confirm("Potvrďte prosím převzetí " + this.selectedResources.length + " zdrojů  od uživatele " + this.selectedReservation.applicant.fullname )) return
      let resources = {}
      this.selectedResources.forEach(res => resources[res.id] = res.comment)
      await API.takeUpResources(this.selectedReservation.id, resources)
      this.selectedResources = []
      this.reservations = await API.getReservations();
      this.selectedReservation = this.reservations.find(r => r.id === this.selectedReservation.id);
    },
    openCalendar() {
      this.calendarDialog = true
    },
    print() {
      this.$refs.pdfCreator.print()
    },
    copy(){
      const resourcesIds = this.selectedReservation.resources.map(res => res.id)
      this.$store.commit('setSelectedResources', resourcesIds)
      this.$router.push({name:'Resources'})
    }

  }
}
</script>

<style>
#reservationTable .v-data-table__wrapper {
  max-height: calc(100vh - 260px);
}
</style>
