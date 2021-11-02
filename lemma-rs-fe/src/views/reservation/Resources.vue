<template lang="pug">
  .flex-grow-1.pa-3(style="height: 0; overflow-y: auto")
    v-progress-circular(v-if="loading" class="d-block mx-auto mt-4" :size="70", :width="4", color="primary" indeterminate)
    div(v-else)
      transition( mode="out-in", name="fade")
        #grid(key="1", v-if="displayStyle === 'cards'")
          v-card.pointer(
            ripple=false
            @click="openResource(resource)",
            :key="resource.id",
            v-for="(resource) in filteredResources",
            max-width="300"
            color="#0000008c"
            class="d-flex flex-column"
          )

            div(style="height: 200px; position:relative")
              div.ma-2(style="position:absolute; z-index: 1")
                v-chip(v-if="!resource.allowed" class="ma-2" label color="#4c0000c2" title="nemáte dostatečné oprávnění")
                  v-icon() mdi-shield-lock
                v-chip(v-if="false" class="ma-2" label color="#4c0000c2" title="Zdroj je ve zvoleném termínu rezervován")
                  v-icon() mdi-lock-clock
                v-chip(v-if="!resource.active" class="ma-2" label color="#4c0000c2" title="Zdroj není k dispozici")
                  v-icon() mdi-heart-broken
                v-chip(v-if="resource.not_returned" class="ma-2" label color="#4c0000c2" title="Zdroj nebyl vrácen")
                  v-icon() mdi-selection-ellipse
                v-chip(v-if="resource.hasTimeConflict" class="ma-2" label color="#4c0000c2" title="Zdroj je již v daném termínu rezervován")
                  v-icon() mdi-clock-alert
                v-chip(v-if="resource.provider !== selectedProvider" class="ma-2" label color="#4c0000c2" :title="'Pro rezervování tohoto zdroje je potřeba vybrat výdejáře:' + resource.providerStr")
                  v-icon() mdi-account-cog
              v-img.rounded-t(height="100%" v-if="resource.image_url" :src="apiUrl + resource.image_url")
              v-img.rounded-t(height="100%" v-else src='@/assets/placeholder.jpg' )
            v-card-title.py-1(style="font-size:1rem; word-break: break-word;") {{resource.name}}
            v-spacer

            v-card-text.subtitle-1.py-1
              tags(:tags="resource.tags_str")
              //div

                //span.ml-1 {{resource.provider_str}}
            v-card-actions
              v-btn(@click.stop="addReservationItem(resource)" :disabled="!resource.reservationIsPossible")
                v-icon(left) mdi-cart-arrow-down
                span(v-if="!resource.selected") Rezervovat
                span(v-else) Odebrat
              v-btn(color=red, @click.stop="openCalendarDialog(resource)", text )
                v-icon(left) mdi-calendar
                | Kalendář
        v-data-table.elevation-1(
          key="2",
          v-else,
          fixed-header,
          height="calc(100vh - 90px)",
          disable-pagination,
          :value="selectedResources"
          hide-default-footer,
          :headers="headers",
          @click:row="rowClick"
          :items="filteredResources",
          item-key="id")
          template(v-slot:item.provider="{ item }") {{item.providerStr}}
          template(v-slot:item.tags="{ item }")
            tags(:tags="item.tags_str")
          template(v-slot:item.required_permission_level="{ item }")
            | {{permissionLevels.find(x => x.level === item.required_permission_level).name}}
          template(v-slot:item.actions="{ item }")
            v-btn(icon, :disabled="!item.reservationIsPossible" @click.stop="addReservationItem(item)" )
              v-icon( small v-if="!item.selected") mdi-cart-arrow-down
              v-icon( small v-else="item.selected") mdi-cart-arrow-up
            v-btn(icon @click.stop="openCalendarDialog(item)")
              v-icon(small) mdi-calendar
          template(v-slot:item.attributes="{ item }")
            v-chip(v-if="!item.allowed" small class="ma-2" label color="#4c0000c2" title="nemáte dostatečné oprávnění")
              v-icon(small) mdi-shield-lock
            v-chip(v-if="false" small class="ma-2" label color="#4c0000c2" title="Zdroj je ve zvoleném termínu rezervován")
              v-icon(small) mdi-lock-clock
            v-chip(v-if="!item.active" small class="ma-2" label color="#4c0000c2" title="Zdroj není k dispozici")
              v-icon(small) mdi-heart-broken
            v-chip(v-if="item.not_returned" small class="ma-2" label color="#4c0000c2" title="Zdroj nebyl vrácen")
              v-icon(small) mdi-selection-ellipse
            v-chip(v-if="item.hasTimeConflict" class="ma-2" label color="#4c0000c2" title="Zdroj je již v daném termínu rezervován")
              v-icon() mdi-clock-alert







    v-dialog(v-model="calendarDialog" max-width="900")
      v-card
        v-toolbar(color="primary", dark)
          v-btn.ma-2(icon, @click="$refs.calendar.prev()")
            v-icon mdi-chevron-left
          span {{ month }}
          v-btn.ma-2(icon, @click="$refs.calendar.next()")
            v-icon mdi-chevron-right
          v-spacer
          v-btn(icon, @click="calendarDialog = false")
            v-icon mdi-close
        v-sheet.pa-2(height=600)
          v-calendar(
            height="400px",
            v-model="value",
            ref="calendar",
            color="primary",
            event-overlap-mode="stack",
            :events="blockingEventsOfActiveResource",
            event-color="cyan",
            type="month"
          )
    v-dialog(v-model="resourceDialog", scrollable :persistent=resourceDialogEditing, max-width="900")
      template(v-slot:default="dialog")
        v-card(color="#131313")
          v-toolbar(color="primary", dark) Zdroj {{activeResource.name}}
            v-spacer
            div(v-if="userRole !== 'COMMON'")
              v-btn(icon, v-if="!resourceDialogEditing" @click="editResource")
                v-icon mdi-pencil
              v-btn(icon, :loading="saveResourceLoading" title="Uložit úpravy" v-else-if="resourceDialogEditing && activeResource.id" @click="saveResource")
                v-icon mdi-content-save
              v-btn(icon, :loading="saveResourceLoading" title="Vytvořit zdroj"  v-else @click="createResource")
                v-icon mdi-plus-circle
            v-btn(icon, @click="resourceDialog = false; resourceDialogEditing = false")
              v-icon mdi-close
          v-card-text.pa-0
            v-container
              v-row
                v-col(cols="12" order="2" order-sm="1" sm="6")
                  v-card.pa-2(style="height:100%")
                    v-form#resource-form
                      v-text-field(v-model="activeResource.name",
                        hide-details,
                        label="Název"
                        :rules="[(v) => !!v || 'Vyplňte jméno zdroje']"
                        prepend-icon="mdi-form-textbox",
                        :disabled="!resourceDialogEditing")
                      api-select(
                        v-model="activeResource.provider"
                        hide-details,
                        prepend-icon="mdi-account-cog",
                        :disabled="!resourceDialogEditing",
                        query="user/?role__in=ADMIN,PROVIDER"
                        :default-index="1",
                        label="Výdejář",
                        :item-value="(itm)=> itm.id" ,
                        :item-text="(itm)=> itm.fullname")
                      v-select.mt-2(prepend-icon="mdi-shield-lock",
                        v-model="activeResource.required_permission_level"
                        :disabled="!resourceDialogEditing",
                        label="Úroveň oprávnění"
                        :item-text="(itm) => itm.name"
                        :item-value="(itm) => itm.level"
                        :items="permissionLevels")
                      v-autocomplete(
                        v-model="activeResource.tags"
                        prepend-icon="mdi-tag", class="mt-0 pt-0",
                        :items="tags",
                        :disabled="!resourceDialogEditing",
                        chips,
                        deletable-chips,
                        small-chips,
                        hide-details,
                        label="Štítky",
                        multiple,
                        :item-value="(itm) => itm.id",
                        :item-text="(itm) => itm.name")
                        template(v-slot:append-item)
                          v-divider
                          v-text-field.px-3(v-model="newTag", label="Nový štítek")
                            template(slot="append")
                              v-btn(icon, @click="createTag")
                                v-icon mdi-plus
                      v-text-field(v-model="activeResource.cost",
                        label="Cena",
                        prepend-icon="mdi-cash-multiple",
                        type="number",
                        :disabled="!resourceDialogEditing")
                        template(slot="append") Kč
                      v-checkbox(prepend-icon="mdi-check-all"
                        class="mt-0"
                        :disabled="!resourceDialogEditing"
                        v-model="activeResource.active"
                        label="Zdroj je k dispozici")
                v-col(cols="12" order="1" order-sm="2" sm="6")
                  v-card.d-flex.align-center.justify-center.pa-2(style="position: relative; height:100%")
                    input(id="image-upload" accept="image/x-png,image/jpeg" :disabled="!resourceDialogEditing" @change="(evt) =>loadImage(evt.target.files)" type="file" style="display: none")
                    label(for="image-upload")
                      img.rounded.w-100(v-if="activeResource.image_url" :style="resourceDialogEditing? 'cursor: pointer' : ''" :src="apiUrl + activeResource.image_url")
                      img.rounded.w-100( v-else :style="resourceDialogEditing? 'cursor: pointer' : ''" src='@/assets/placeholder.jpg' )
                      div(v-if="resourceDialogEditing" style="position: absolute; right:10px; bottom:10px")
                        v-btn.mr-2(small fab @click="pasterActive = true" )
                          v-icon(small) mdi-content-paste
                        v-btn(fab small @click="activeResource.image_url = ''")
                          v-icon(small) mdi-image-remove
              v-row
                v-col()
                  v-tabs.secondary.darken-2(v-model="resourceDetailTab" background-color="secondary darken-2")
                    v-tab Popis
                    v-tab(v-if="userRole !== 'COMMON'") Interní poznámky
                    v-tab(v-if="userRole !== 'COMMON'") Inventární čísla
                  v-tabs-items.secondary.darken-2(v-model="resourceDetailTab")
                    v-tab-item(style="background-color:#1E1E1E")
                      div.ma-3(v-if="!resourceDialogEditing" v-html="activeResource.description")
                      vue-editor(v-else v-model="activeResource.description" :editor-toolbar="toolbarOptions")
                    v-tab-item(style="background-color:#1E1E1E")
                      div.ma-3(v-if="!resourceDialogEditing" v-html="activeResource.internal_notes")
                      vue-editor(v-else v-model="activeResource.internal_notes" :editor-toolbar="toolbarOptions")
                    v-tab-item
                      v-list
                        v-list-item(v-for='invNumber in activeResource.inv_numbers' :key='invNumber')
                          v-list-item-icon
                            v-icon mdi-numeric
                          v-list-item-content
                            v-list-item-title(v-text='invNumber')
                          v-list-item-avatar
                            v-btn(v-if="resourceDialogEditing" @click='removeInvNumber(invNumber)' fab='' x-small dark)
                              v-icon mdi-delete
                        v-divider
                        v-list-item(v-if="resourceDialogEditing")
                          v-list-item-content
                            v-list-item-title
                              v-text-field(v-model="newInvNumber",
                                label="Nové inventární čislo",
                                prepend-icon="mdi-numeric",
                              )
                          v-list-item-avatar
                            v-btn(color='success' @click='addInvNumber' fab='' x-small='' dark='')
                              v-icon mdi-plus-circle




    paster(:enable="pasterActive" @close="handlePaste")
    portal(to='add-resource-btn')
      v-btn.mb-3(color="primary", block @click="createResourceDialog") Přidat zdroj
</template>

<script>
import API from "@/model/httpclient";
import {VueEditor} from "vue2-editor";
import Tags from "@/components/Tags"
import Paster from "@/components/Paster";
import ApiSelect from "@/components/ApiSelect";

const emptyResource = () => {
  return {
    name: "",
    description: "",
    internal_notes: "",
    cost: 0,
    image_url: null,
    tags: [],
    provider: null,
    required_permission_level: 1,
    invNumbers: []
  };
};

export default {
  props: ["displayStyle"],
  components: {
    Tags,
    VueEditor,
    Paster,
    ApiSelect
  },
  async mounted() {
    this.loading = true
    await this.loadTags()
    await this.loadPermissionLevels()
    await this.$store.dispatch('getProviders')
    await this.$store.dispatch('getProjects')
    await this.$store.dispatch('getResources')
    this.loading = false

  },
  computed: {
    month() {
      return new Date(this.value).toLocaleString("cs-CZ", {month: "long"});
    },
    userRole() {
      return this.$store.getters.getDisplayRole
    },
    filteredResources() {
      return this.$store.getters.filteredResources
    },
    selectedResources() {
      return this.$store.state.reservation.selectedResources
    },
    selectedProvider() {
      return this.$store.state.reservation.provider
    },
    providers() {
      return this.$store.state.providers
    },
    apiUrl() {
      return process.env.VUE_APP_API_URL
    },
  },
  methods: {
    addReservationItem(item) {
      this.$store.commit('toggleSelectedItem', item)
    },
    rowClick(item, row) {

      this.activeResource = {...item};
      this.resourceDialog = true

    },
    createResourceDialog() {
      this.activeResource = emptyResource()
      this.resourceDialogEditing = true
      this.resourceDialog = true
    },
    openResource(resource) {
      this.activeResource = JSON.parse(JSON.stringify(resource))
      this.resourceDialog = true
    },
    editResource() {
      this.resourceDialogEditing = true;
    },
    async loadImage(files) {
      const file = files[0]
      if (!file) return;
      //this.activeResource.image = evt.target.files[0]
      const formData = new FormData();
      formData.append('file', file);
      this.activeResource.image_url = await API.uploadImage(formData, file.name)

    },
    handlePaste(files) {
      this.pasterActive = false;
      this.loadImage(files)
    },
    async loadTags() {
      this.tags = await API.getTags()
    },
    async loadProviders() {
      this.providers = await API.getUsers('PROVIDER,ADMIN')

    },

    async loadPermissionLevels() {
      this.permissionLevels = await API.getPermissionLevels()
      console.log(this.permissionLevels)
    },
    async createResource() {
      try {
        this.saveResourceLoading = true
        this.activeResource = await API.createResource(this.activeResource);
        await this.$store.dispatch('getResources')
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Zdroj vytvořen",
        });
      } catch (e) {
        console.log(e)
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Vytváření zdroje selhalo",
        });

      }
      this.saveResourceLoading = false
    },
    async saveResource() {
      this.saveResourceLoading = true
      try {

        await API.updateResource(this.activeResource);
        await this.$store.dispatch('getResources')
        this.resourceDialogEditing = false
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Zdroj uložen",
        });
      } catch (e) {
        console.log(e)
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládání zdroje selhalo",
        });

      }
      this.saveResourceLoading = false
    },
    async createTag() {
      try {
        await API.createTag(this.newTag);
        await this.loadTags();
        this.newTag = '';
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Štítek vytvořen",
        });
      } catch (e) {
        console.log(e)
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Vytváření štítku selhalo",
        });

      }

    },
    addInvNumber() {
      if (this.activeResource.inv_numbers.indexOf(this.newInvNumber) === -1) {
        this.activeResource.inv_numbers.push(this.newInvNumber)
        this.newInvNumber = ''
      }


    },
    removeInvNumber(value) {
      this.activeResource.inv_numbers = this.activeResource.inv_numbers.filter(function (item) {
        return item !== value
      })
      console.log('inv number removed')
    },
    openCalendarDialog(resource) {
      this.activeResource = resource
      this.calendarDialog = true
      this.blockingEventsOfActiveResource = this.activeResource.blocking_reservations.map(blockingRes => {
        return {
          color: this.$randomColor({seed: blockingRes.reservation_name, luminosity: 'dark'}),
          end: new Date(blockingRes.end),
          start: new Date(blockingRes.start),
          name: blockingRes.reservation_name,
          timed: true
        }
      })
    }
  },
  data() {
    return {
      loading: false,
      value: new Date(),
      resourceDetailTab: 0,
      tags: [],
      newTag: '',
      newInvNumber: '',
      blockingEventsOfActiveResource: [],
      permissionLevels: [],
      calendarDialog: false,
      resourceDialog: false,
      resourceDialogEditing: false,
      activeResource: emptyResource(),
      headers: [
        {text: "Jméno", value: "name"},
        {text: "Výdejář", value: "provider"},
        {text: "Oprávnění", value: "required_permission_level"},
        {text: "Tagy", value: "tags"},
        {text: "Atributy", value: "attributes"},
        {text: "Akce", value: "actions", sortable: false},
      ],
      saveResourceLoading: false,
      pasterActive: false,
      toolbarOptions: [
        [{'header': [1, 2, 3, 4, 5, 6, false]}],  // custom dropdown
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        [{'list': 'ordered'}, {'list': 'bullet'}],
        ['clean']                                         // remove formatting button
      ]
    };
  },
};
</script>

<style lang="scss">
#resource-form {
  .v-select__selection--disabled, .theme--dark.v-input--is-disabled, .v-icon--disabled, .theme--dark.v-input--is-disabled input, .v-icon, .v-chip__content {
    color: white !important;
  }

  .v-label--is-disabled {
    color: rgba(255, 255, 255, 0.7) !important;
  }

  .v-input--is-disabled.v-select .v-input__append-inner {
    display: none;
  }

  .v-chip--disabled {
    opacity: 1;
  }

}

.ql-toolbar.ql-snow {
  border: none;
}

#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-gap: 16px;
  justify-content: center;
  width: 100%;

}

table {
  th {
    white-space: nowrap !important;
  }
}
</style>
