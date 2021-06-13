<template lang="pug">
  v-main
    v-container
      v-card
        v-tabs()
          v-tab(v-if="userRole !== 'COMMON'", href="#pending") Ke schválení
          v-tab(href="#my")  Moje rezervace
          v-tab(v-if="userRole !== 'COMMON'", @change="tab='all'")  Plánované
          v-tab(v-if="userRole !== 'COMMON'", @change="tab='all'")  Vše

      v-data-table.elevation-1.pointer-rows(:headers='headers'
        :items='filteredItems'
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
            v-btn(color='primary' @click.stop='openCalendar')
              | Kalendář
        template(v-slot:item.approved='{ item }')
          v-icon {{ item.approved !== null ?  (item.approved ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline") : "mdi-help-box" }}
        template(v-slot:item.actions='{ item }')
          v-btn.mr-1(color="primary")
            v-icon(left @click="openReservationDialog(item)") mdi-handshake
            | vydat
          v-btn.mr-1(color="warning")
            v-icon(left @click="openReservationDialog(item)") mdi-delete-circle
            | storno
          v-btn.mr-1(v-if="true" color="success")
            v-icon(left @click="openReservationDialog(item)") mdi-check-circle
            | schválit {{item.approved === null}}
          v-btn.mr-1(color="error")
            v-icon(left @click="openReservationDialog(item)") mdi-close-circle
            | zamítnout
      v-dialog(v-model="calendarDialog")
      v-card
        v-toolbar(color="primary", dark)
          v-btn.ma-2(
            icon,
            @click="$refs.calendar.prev() "
          )
            v-icon mdi-chevron-left
          span.text-center(style='width:110px') {{ calendarMonth }}
          v-btn.ma-2(icon, @click="$refs.calendar.next()")
            v-icon mdi-chevron-right
          v-spacer
          v-btn(icon, @click="calendarDialog = false")
            v-icon mdi-close
        v-sheet.pa-2
          v-calendar(
            v-model="calendarModel",
            ref="calendar",
            color="primary",
            :events="calendarEvents",
            type="month"
          )
      v-dialog(max-width="800px" v-model="reservationDialog")
        v-toolbar(color="primary")
          | Rezervace
          v-spacer
          v-btn(icon, @click="reservationDialog = false")
            v-icon mdi-close
        v-sheet.pa-2(v-if="reservationDialog===true")
          v-data-table(:items='formatedResources', :headers='resourcesHeaders' show-select=true)
            template(v-slot:top)
              v-toolbar(flat)
                v-btn(color='primary' @click.stop='openCalendar')
                  | převzít
                v-btn(color='primary' @click.stop='openCalendar')
                  | odebrat


</template>

<script>
import API from "@/model/httpclient";

const emptyRequest = () => {
  return {
    requestedLevel: 1,
    reason: ''
  }
}

export default {
  name: "Reservations",
  data: function () {
    return {
      evts: this.getEvents(new Date('2021-01-05'), new Date('2021-05-30')),
      calendarDialog: false,
      reservationDialog: false,
      selectedReservation: null,
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
        {text: 'Akce', value: 'actions'}

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
          name: res.applicant + ' - ' + res.project,
          timed: true
        }
      })
    },
    calendarMonth() {
      return new Date(this.calendarModel).toLocaleString("cs-CZ", {month: "long", year: 'numeric'});
    },
    filteredItems() {
      return this.reservations.filter(itm => {
        if (this.tab === 'my') return itm.applicant.id === this.$store.getters.getProfile.id
        if (this.tab === 'pending') return !itm.expiration_date
        return true
      }).map(itm => {
        return {
          ...itm,
          pickup_date_time: this.$moment(itm.pickup_date_time).locale("cs").format('LLL'),
          return_date_time: this.$moment(itm.return_date_time).locale("cs").format('LLL')
        }
      })
    },
    formatedResources() {
      return this.selectedReservation?.resources.map(res => {
        return {
          ...res,
         real_pickup_date: res.real_pickup_date ? this.$moment(res.real_pickup_date).locale("cs").format('LLL') : 'nevyzvednuto',
         real_return_date: res.real_return_date ? this.$moment(res.real_return_date).locale("cs").format('LLL') : 'nevráceno'
        }
      })
    },
    userRole() {
      return this.$store.getters.getDisplayRole
    },
    headers() {
      const headers = [
        {text: "Žadatel", value: "applicant"},
        {text: "Od", value: "pickup_date_time"},
        {text: "Do", value: "return_date_time"},
        {text: "Schváleno", value: "approved"},
        {text: "Vyzvednuto", value: "picked_up"},
        {text: "Akce", value: "actions", sortable: false},
      ]
      if (this.$store.getters.getDisplayRole === 'COMMON') headers.pop()
      return headers
    },
  },
  methods: {
    openReservationDialog(reservation) {
      console.log(reservation)
      this.selectedReservation = reservation
      this.reservationDialog = true
    },
    getEvents(start, end) {
      const events = []

      const min = new Date(`2021-05-12T00:00:00`)
      const max = new Date(`2021-05-30T23:59:59`)
      const days = (max.getTime() - min.getTime()) / 86400000
      const eventCount = this.rnd(days, days + 20)

      for (let i = 0; i < eventCount; i++) {
        const allDay = this.rnd(0, 3) === 0
        const firstTimestamp = this.rnd(min.getTime(), max.getTime())
        const first = new Date(firstTimestamp - (firstTimestamp % 900000))
        const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
        const second = new Date(first.getTime() + secondTimestamp)

        events.push({
          name: 'dawdaw',
          start: first,
          end: second,
          color: 'cyan',
          timed: !allDay,
        })
      }

      return events
    },
    getEventColor(event) {
      return event.color
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    openCalendar() {
      this.calendarDialog = true
    }
    //   openCreateDialog() {
    //     if (this.$refs.createPermissionRequestForm) this.$refs.createPermissionRequestForm.resetValidation()
    //     this.newRequest = emptyRequest()
    //     this.createDialog = true
    //   },
    //   openResolveDialog(id, approved) {
    //     if (this.$refs.resolvePermissionRequestForm) this.$refs.resolvePermissionRequestForm.resetValidation()
    //     this.newResolve = emptyResolve(id, approved)
    //     this.resolveDialog = true
    //   },
    //   async resolve() {
    //     const date = this.newResolve.expirationDate ? new Date(this.newResolve.expirationDate) : null
    //     try {
    //       await API.resolvePermissionRequest(this.newResolve.id,date, this.newResolve.approved,this.newResolve.response)
    //       this.permissions = await API.getPermissionRequests();
    //       this.$store.dispatch("notify", {
    //         type: "success",
    //         text: "Žádost vyřešena",
    //       });
    //       console.log('zaviram')
    //     } catch (e) {
    //       console.log(e);
    //       this.$store.dispatch("notify", {
    //         type: "error",
    //         text: "Ukládání žádosti se nezdařilo ",
    //       });
    //     } finally {
    //       console.log('zaviram')
    //       this.resolveDialog = false;
    //     }
    //
    //
    //   },
    //   async create() {
    //     if (!this.$refs.createPermissionRequestForm.validate()) return;
    //     try {
    //       await API.applyPermissionRequest(this.newRequest.requestedLevel, this.newRequest.reason)
    //       this.permissions = await API.getPermissionRequests()
    //       this.createDialog = false;
    //       await this.$store.dispatch("notify", {
    //         type: "success",
    //         text: "Žádost vytvořena",
    //       });
    //     } catch (e) {
    //       console.log(e);
    //       await this.$store.dispatch("notify", {
    //         type: "error",
    //         text: "Vytváření žádosti selhalo",
    //       });
    //     }
    //
    //   }
  }
}
</script>

<style scoped>

</style>
