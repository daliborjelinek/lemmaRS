<template lang="pug">
  v-dialog(v-model="userDialog" scrollable max-width="900px")
    v-card( )
      v-toolbar(color="primary", dark)
        | {{ user.profile.fullname }}
        v-chip.ma-2
          v-icon.mr-2(small) mdi-account-circle-outline
          | {{ currentUserRole }}
        v-spacer
        v-btn(icon, :loading="saveUserLoading" title="Uložit úpravy"  @click="save")
          v-icon mdi-content-save
        v-btn(icon, @click="userDialog = false")
          v-icon mdi-close
      v-card-text.pa-0
        v-container
          v-tabs(v-model="tab" v-if="role_display !== 'COMMON'")
            v-tab Údaje
            v-tab(v-if="role_display !== 'COMMON'") Dostupnost
            v-tab(v-if="role_display !== 'COMMON'") Dovolená
          v-tabs-items(v-model="tab")
            v-tab-item
              v-form.mt-2
                v-select(v-if="currentUserRole !== 'COMMON'" v-model='role_display' :items='role' label='Zobrazit GUI jako')
                v-text-field(v-model='email' label='E-mail' required='')
                v-text-field(label='Telefon' v-model='phone')
                v-textarea(name='Adresa' label='Adresa' v-model='address' hint='Adresa')
                v-text-field(v-if="role_display !== 'COMMON'" label='Místnost' v-model='room')
                v-checkbox.ml-2(v-if="role_display !== 'COMMON'" label='Zasílat upozorněni o žádostech o oprávnění' v-model='send_notification_on_permission_request')
                v-checkbox.ml-2(v-if="role_display !== 'COMMON'" label='Zasílat upozorněni o žádostech o schválení rezervace' v-model='send_notification_on_reservation_request')
            v-tab-item
              v-sheet.mt-2(rounded)
                w-h-calendar(:init='user.profile.calendar_data' v-model="eventsParent")
            v-tab-item
              v-data-table(:headers="holidayHeaders", :items="user.profile.holidays")
                template(v-slot:top)
                  v-toolbar.mt-2(flat)
                    v-spacer
                    v-dialog( v-model='showCalendar' width='290px')
                      template(v-slot:activator='{ on, attrs }')
                        v-btn(
                          color="primary"
                          v-bind='attrs'
                          v-on='on') Nový záznam
                      v-date-picker(first-day-of-week='1' :min='$moment().format()' v-model='datePickerDate'  no-title range scrollable)
                        v-spacer
                        v-btn(text='' color='primary' @click='addHolidayRecord')
                          | OK
                template(v-slot:item.actions='{ item }')
                    v-btn.mr-1( icon color="warning" @click.stop="removeHolidayRecord(item)")
                      v-icon mdi-delete-circle
                template(v-slot:item.from='{ item }')
                  | {{$moment(item.from).locale("cs").format('LL')}}
                template(v-slot:item.to='{ item }')
                  | {{$moment(item.to).locale("cs").format('LL')}}

</template>
<script>
import {createHelpers} from "vuex-map-fields";
import {USER_UPDATE} from "@/store/actions/user";
import WHCalendar from "@/components/WHCalendar";

const {mapFields} = createHelpers({
  getterType: "getUserField",
  mutationType: "updateUserField",
});
export default {
  name: 'user',
  components: {WHCalendar},
  data: () => ({
    datePickerDate: [],
    userDialog: false,
    showCalendar: false,
    holidayHeaders: [{
      text: 'od',
      value: 'from'
    }, {
      text: 'do',
      value: 'to'
    }, {
      text: 'akce',
      value: 'actions'
    },],
    tab: null,
    saveUserLoading: false,
    eventsParent: [],
  }),
  computed: {
    currentUserRole() {
      return this.$store.getters.getRole;
    },
    user() {
      return this.$store.state.user
    },
    ...mapFields([
      "profile.address",
      "profile.phone",
      "profile.email",
      "profile.role_display",
      "profile.role",
      "profile.room",
      "profile.send_notification_on_permission_request",
      "profile.send_notification_on_reservation_request"
    ]),
    role() {
      return [
        {
          text: "Admin",
          value: "ADMIN",
          disabled: this.currentUserRole !== "ADMIN",
        },
        {text: "Běžný  uživatel", value: "COMMON"},
        {text: "Výdejář", value: "PROVIDER"},
      ];
    },
  },
  methods: {
    async save() {
      this.saveUserLoading = true
      this.$store.commit('setCalendar', this.eventsParent)
      await this.$store.dispatch(USER_UPDATE);
      this.saveUserLoading = false

    },
    show() {
      this.userDialog = true
    },
    addHolidayRecord() {
        const sorted  = this.datePickerDate.sort((a,b) => this.$moment(a) - this.$moment(b))
        let from, to
        if(!sorted.length) return
        if(sorted.length === 1){
          from = to = sorted[0]
        }
        else {
          from = sorted[0]
          to = sorted[1]
        }
        from = this.$moment(from).toISOString()
        to = this.$moment(to).endOf('day').toISOString()
        this.$store.commit('addHolidayRecord',{from, to})
        this.showCalendar = false
        this.datePickerDate = []
    },
    removeHolidayRecord(record){
      this.$store.commit('removeHolidayRecord',record)
    }
  },
};
</script>

<style type="scss">
#wh-calendar .v-calendar-daily_head-day-label {
  display: none;
}

#wh-calendar {
  border-left: none !important;
  border-top: none !important;
}

</style>
