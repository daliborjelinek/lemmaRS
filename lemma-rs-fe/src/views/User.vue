<template lang="pug">
  v-dialog(v-model="userDialog" scrollable max-width="900px")
    v-card( )
      v-toolbar(color="primary", dark)
        | {{ $store.state.user.profile.fullname }}
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
          v-tabs(v-model="tab")
            v-tab Údaje
            v-tab Dostupnost
            v-tab Dovolená
          v-tabs-items(v-model="tab")
            v-tab-item
              v-form.mt-2
                v-select(v-if="currentUserRole !== 'COMMON'" v-model='role_display' :items='role' label='Zobrazit GUI jako')
                v-text-field(v-model='email' label='E-mail' required='')
                v-text-field(label='Telefon' v-model='phone')
                v-text-field(label='Místnost' v-model='phone')
                v-textarea(name='Adresa' label='Adresa' v-model='address' hint='Adresa')
            v-tab-item
              v-sheet.mt-2(rounded)
                w-h-calendar(:init='$store.state.user.profile.calendar_data' v-model="eventsParent")
            v-tab-item
              v-data-table
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
    userDialog: true,
    tab: null,
    saveUserLoading: false,
    eventsParent: [],
  }),
  computed: {
    currentUserRole() {
      return this.$store.getters.getRole;
    },
    ...mapFields([
      "profile.address",
      "profile.phone",
      "profile.email",
      "profile.role_display",
      "profile.role",
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
