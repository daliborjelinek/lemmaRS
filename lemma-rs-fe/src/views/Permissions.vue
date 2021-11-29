<template lang="pug">
  v-main
    v-container
      v-card
        v-tabs(v-model="tab")
          v-tab(v-if="userRole !== 'COMMON'", href="#pending" ) Ke schválení
          v-tab(@change="tab='my'" href="#my")  Moje oprávnění
          v-tab(v-if="userRole !== 'COMMON'", href="#all")  Vše
      v-data-table.elevation-1(:headers='headers'
        :items='filteredItems'
        :search='search'
        :footer-props="{'items-per-page-options': [10, 50, 100]}"
        :items-per-page='50')
        template(v-slot:top)
          v-toolbar(flat='')
            v-text-field(style='max-width: 300px'
              v-model='search'
              append-icon='mdi-magnify'
              label='Hledat'
              single-line=''
              hide-details='')
            v-spacer
            v-btn(color='primary' @click.stop='openCreateDialog')
              | Vytvořit žádost
        template(v-slot:item.approved='{ item }')
          v-icon(v-if="item.approved === null") mdi-help-box
          v-icon(v-else-if="item.approved === false" color='error') mdi-close-box
          v-icon(v-else color='success') mdi-checkbox-marked
        template(v-slot:item.applicant='{ item }')
          | {{item.applicant.fullname}}
        template(v-slot:item.actions='{ item }')
          span(v-if="item.approved === null")
            v-btn(icon color="green")
              v-icon( @click="openResolveDialog(item, true)") mdi-check-decagram
            v-btn(icon color="red")
              v-icon( @click="openResolveDialog(item, false)") mdi-close-octagon-outline

        template(v-slot:item.expiration_date='{ item }')
          span( v-if="item.expiration_date" :style="{ color: $moment(item.expiration_date) > new Date() ?'#36a436' : '#c74848'}") {{$moment(item.expiration_date).locale("cs").format('LLL') }}

    v-dialog(v-model='createDialog' max-width='500')
      v-card(v-if="userHasFilledRequiredDetails")
        v-card-title.headline Žádost o přidělení oprávnění
        v-card-text
          v-form(ref='createPermissionRequestForm' lazy-validation)
            v-text-field(v-model='newRequest.reason' :rules="[(v) => !!v || 'Vyplňte důvod žádosti']" label='Důvod')
            v-select(
              v-model="newRequest.requestedLevel"
              label="Požadovaná úroveň oprávnění"
              :item-text="(itm) => itm.name"
              :item-value="(itm) => itm.level"
              :items="permissionLevels")
            v-alert(class="mb-0"
              v-if="newRequest.requestedLevel > 1"
              dense
              icon="mdi-alert"
              text
              type="warning") Pro udělení tohoto oprávnění je potřeba poskytnout potvrení o pojištění. Vice informaci v FAQ
        v-divider
        v-card-actions
          v-spacer
          v-btn(text='' @click='createDialog = false')  zavřít
          v-btn(text='' @click='create')  Odeslat
      v-card(v-else)
        v-card-title.headline Chyba
        v-card-text Pro podání žádosti je nutné vyplnit v uživatelském profilu e-mail, tel. číslo a adresu

    v-dialog(v-model='resolveDialog' max-width='500')
      v-card
        v-card-title.headline
          span(v-if="newResolve.approved") Schválení požadavku
          span(v-else) Zamítnutí požadavku
        v-card-text
          v-form(ref='resolvePermissionRequestForm' lazy-validation)
            v-text-field(v-model='newResolve.response',  label='Důvod')
            v-menu(v-if="newResolve.approved" v-model="datepicker" :close-on-content-click='false' :nudge-right='40' transition='scale-transition' offset-y='' min-width='auto')
              template(v-slot:activator='{ on, attrs }')
                v-text-field(v-model='newResolve.expirationDate' label='Datum expirace' readonly v-bind='attrs' v-on='on')
              v-date-picker(v-model='newResolve.expirationDate' @input='datepicker = false')
        v-divider
        v-card-actions
          v-spacer
          v-btn(text @click='resolveDialog = false')  zavřít
          v-btn(text @click='resolve')  Odeslat


</template>

<script>
import API from "@/model/httpclient";

const emptyRequest = () => {
  return {
    requestedLevel: 1,
    reason: ''
  }
}
const emptyResolve  = (id, approved) => {
  return {
    approved,
    expirationDate: approved ? new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().substr(0, 10) : null,
    response: '',
    id
  }
}
export default {
  name: "Permissions",
  data: function () {
    return {
      datepicker: false,
      newRequest: emptyRequest(),
      newResolve: emptyResolve(true),
      tab: 'pending',
      createDialog: false,
      resolveDialog: false,
      search: '',
      permissions: [],
      permissionLevels: [],
      loading: true,


    }
  },
  async created() {
    this.permissionLevels = await API.getPermissionLevels()

    this.permissions = await API.getPermissionRequests()
    this.loading = false

  },
  computed: {
    filteredItems() {
      return this.permissions.filter(itm => {
        if(this.tab === 'my') return itm.applicant.id === this.$store.getters.getProfile.id
        if(this.tab === 'pending') return itm.approved === null
        return true
      }).map(itm => {
        return {
          approved: itm.approved,
          applicant: itm.applicant,
          requested_level: itm.requested_level.name,
          created_at: this.$moment(itm.created_at).locale("cs").format('LLL'),
          expiration_date: itm.expiration_date,
          reason: itm.reason,
          reply: itm.reply,
          id: itm.id
        }

      })
    },
    userRole() {
      return this.$store.getters.getDisplayRole
    },
    userHasFilledRequiredDetails(){
      const profile = this.$store.state.user.profile
      return profile.address !== '' && profile.phone !== '' && profile.email !== ''
    },
    headers(){
     const headers = [
        {text: "Žadatel", value: "applicant"},
        {text: "Level", value: "requested_level"},
        {text: "Vytvořeno", value: "created_at"},
        {text: "Důvod", value: "reason"},
        {text: "Expirace", value: "expiration_date"},
        {text: "Odpověď", value: "response"},
        {text: "Výsledek", value: "approved"},
        {text: "Akce", value: "actions", sortable: false},
      ]
      if(this.$store.getters.getDisplayRole === 'COMMON') headers.pop()
      return headers
    }


  },
  methods: {
    openCreateDialog() {
      if (this.$refs.createPermissionRequestForm) this.$refs.createPermissionRequestForm.resetValidation()
      this.newRequest = emptyRequest()
      this.createDialog = true
    },
    openResolveDialog(itm, approved) {
      if (this.$refs.resolvePermissionRequestForm) this.$refs.resolvePermissionRequestForm.resetValidation()
      this.newResolve = emptyResolve(itm.id, approved)
      this.resolveDialog = true
    },
    async resolve() {
      const date = this.newResolve.expirationDate ? new Date(this.newResolve.expirationDate) : null
      try {
        await API.resolvePermissionRequest(this.newResolve.id,date, this.newResolve.approved,this.newResolve.response)
        this.permissions = await API.getPermissionRequests()
        this.resolveDialog = false;
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Žádost vyřešena",
        });
      } catch (e) {
        console.log(e);
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládání žádosti se nezdařilo ",
        });
      }

    },
    async create() {
      if (!this.$refs.createPermissionRequestForm.validate()) return;
      try {
        await API.applyPermissionRequest(this.newRequest.requestedLevel, this.newRequest.reason)
        this.permissions = await API.getPermissionRequests()
        this.createDialog = false;
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Žádost vytvořena",
        });
      } catch (e) {
        console.log(e);
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Vytváření žádosti selhalo",
        });
      }

    }
  }
}
</script>

<style scoped>

</style>
