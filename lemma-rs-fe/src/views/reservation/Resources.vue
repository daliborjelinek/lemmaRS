<template lang="pug">
  .flex-grow-1.pa-3(style="height: 0; overflow-y: auto")
    transition(mode="out-in", name="fade")
      #grid(key="1", v-if="displayStyle === 'cards'")
        v-card.pointer(
          ripple=false
          @click="openResource(resource)",
          :key="resource.id",
          v-for="(resource, index) in filteredResources",
          max-width="300"
          color="#0000008c"
          class="d-flex flex-column"
        )

          div(style="height: 200px")
            v-img.rounded-t(height="100%" v-if="resource.image_url" :src="apiUrl + resource.image_url")
            v-img.rounded-t(height="100%" v-else src='@/assets/placeholder.jpg' )
          v-card-title.py-1(style="word-break: break-word;") {{resource.name}}
          v-spacer

          v-card-text.subtitle-1.py-1
            v-icon mdi-tag
            tags(:tags="resource.tags_str")
            div
              v-icon mdi-account-cog
              span.ml-1 {{resource.provider_str}}
          v-card-actions
            v-btn(@click.stop="addReservationItem(resource)" )
              v-icon(left) mdi-cart-arrow-down
              span(v-if="!resource.selected") Rezervovat
              span(v-else) Odebrat
            v-btn(color=red, @click.stop="dialog = true", text )
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
        template(v-slot:item.provider="{ item }") {{providers.find(x => x.id === item.provider).fullname}}
        template(v-slot:item.tags="{ item }")
          tags(:tags="item.tags_str")
        template(v-slot:item.actions="{ item }")
          v-btn(@click.stop="dialog = true", text )
            v-icon(left) mdi-calendar



    v-dialog(v-model="dialog")
      v-card
        v-toolbar(color="primary", dark)
          span Canon EOD 500D
          v-btn.ma-2(
            icon,
            @click="$refs.calendar.prev(); click($refs.calendar); "
          )
            v-icon mdi-chevron-left
            span {{ month }}
          v-btn.ma-2(icon, @click="$refs.calendar.next()")
            v-icon mdi-chevron-right
          v-spacer
            v-btn(icon, @click="dialog = false")
              v-icon mdi-close
        v-sheet.pa-2(height="400")
          v-calendar(
            v-model="value",
            ref="calendar",
            color="primary",
            :events="events",
            event-color="cyan",
            type="month"
          )
    v-dialog(v-model="resourceDialog", :persistent=resourceDialogEditing, max-width="900")
      template(v-slot:default="dialog")
        v-card
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
          v-card-text
            v-row
              v-col()
                input(id="image-upload" accept="image/x-png,image/jpeg" :disabled="!resourceDialogEditing" @change="(evt) =>loadImage(evt.target.files)" type="file" style="display: none")
                label(for="image-upload")
                  div(style="position: relative")
                    v-img.rounded( v-if="activeResource.image_url" :style="resourceDialogEditing? 'cursor: pointer' : ''" :src="apiUrl + activeResource.image_url")
                    v-img.rounded( v-else :style="resourceDialogEditing? 'cursor: pointer' : ''" src='@/assets/placeholder.jpg' )
                    div(v-if="resourceDialogEditing" style="position: absolute; right:10px; bottom:10px")
                      v-btn.mr-2(small fab @click="pasterActive = true" )
                        v-icon(small) mdi-content-paste
                      v-btn(fab small @click="activeResource.image_url = ''")
                        v-icon(small) mdi-image-remove
              v-col
                v-form#resource-form
                  v-text-field(v-model="activeResource.name",
                    hide-details,
                    label="Název"
                    :rules="[(v) => !!v || 'Vyplňte jméno zdroje']"
                    prepend-icon="mdi-form-textbox",
                    :disabled="!resourceDialogEditing")
                  v-select(prepend-icon="mdi-account-cog",
                    v-model="activeResource.provider"
                    hide-details,
                    :disabled="!resourceDialogEditing",
                    label="Výdejář",
                    :item-value="(itm)=> itm.id" ,
                    :item-text="(itm)=> itm.fullname"
                    :items="providers")
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

            v-divider
            v-row

              v-col(class="pt-0")
                v-tabs(v-model="resourceDetailTab" class="mb-3")
                  v-tab Popis
                  v-tab(v-if="userRole !== 'COMMON'") Interní poznámky
                v-tabs-items(v-model="resourceDetailTab")
                  v-tab-item
                    div(v-if="!resourceDialogEditing" v-html="activeResource.description")
                    vue-editor(v-else v-model="activeResource.description" :editor-toolbar="toolbarOptions")
                  v-tab-item
                    div(v-if="!resourceDialogEditing" v-html="activeResource.internal_notes")
                    vue-editor(v-else v-model="activeResource.internal_notes" :editor-toolbar="toolbarOptions")

    paster(:enable="pasterActive" @close="handlePaste")
    portal(to='add-resource-btn')
      v-btn.mb-3(color="primary", block @click="createResourceDialog") Přidat zdroj
</template>

<script>
import API from "@/model/httpclient";
import {VueEditor} from "vue2-editor";
import Tags from "@/components/Tags"
import Paster from "@/components/Paster";

const emptyResource = () => {
  return {
    name: "",
    description: "",
    internal_notes: "",
    cost: 0,
    image_url: null,
    tags: [],
    provider: null,
    required_permission_level: 1
  };
};

export default {
  props: ["displayStyle"],
  components: {
    Tags,
    VueEditor,
    Paster
  },
  async mounted() {

    await this.loadTags()
    await this.loadProviders()
    await this.loadPermissionLevels()
    await this.$store.dispatch('getProjects')
    await this.$store.dispatch('getResources')


  },
  computed: {
    month() {
      console.log(
          new Date(this.value).toLocaleString("cs-CZ", {month: "long"})
      );
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
    apiUrl() {
      return process.env.VUE_APP_API_URL
    },
  },
  methods: {
    click(props) {
      console.log(props);
    },
    addReservationItem(item){
      this.$store.commit('toggleSelectedItem',item)
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
      this.activeResource = {...resource};
      this.resourceDialog = true
    },
    editResource() {
      this.resourceDialogEditing = true;
    },
    async loadImage(files) {
      const file = files[0]
      if(!file) return;
      //this.activeResource.image = evt.target.files[0]
      const formData = new FormData();
      formData.append('file', file);
      const url = await API.uploadImage(formData, file.name)
      this.activeResource.image_url = url

    },
    handlePaste(files){
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

    }

  },
  data() {
    return {
      value: new Date(),
      resourceDetailTab: 0,
      tags: [],
      newTag: '',
      providers: [],
      permissionLevels: [],
      events: [
        {
          color: "cyan",
          end: new Date("2021-02-12"),
          name: "Ondřej Kocar - Onetake",
          start: new Date("2021-02-8"),
          timed: false,
        },
      ],
      dialog: false,
      resourceDialog: false,
      resourceDialogEditing: false,
      activeResource: emptyResource(),
      headers: [
        {text: "Jméno", value: "name"},
        {text: "Výdejář", value: "provider"},
        {text: "Oprávnění", value: "required_permission_level_str"},
        {text: "Tagy", value: "tags"},
        {text: "Dostupné", value: "active"},
        {text: "Akce", value: "actions", sortable: false},
      ],
      saveResourceLoading: false,
      pasterActive:false,
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

.ql-toolbar.ql-snow, ql-container.ql-snow {
  border: none;
}

#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-gap: 16px;
  justify-content: center;
  width: 100%;
}
#reservation-items{
  th {
    white-space: nowrap !important;
  }
}
</style>
