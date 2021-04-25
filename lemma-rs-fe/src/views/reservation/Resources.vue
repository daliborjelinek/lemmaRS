<template lang="pug">
  .flex-grow-1.pa-3(style="height: 0; overflow-y: auto")
    transition(mode="out-in", name="fade")
      #grid(key="1", v-if="displayStyle === 'cards'")
        v-card.pointer(
          @click="openResource(item)",
          v-ripple="",
          :key="index",
          v-for="(item, index) in 20",
          max-width="300"
        )
          v-img(
            height="200",
            :src="'https://picsum.photos/300/250?random=' + index"
          )
          v-card-title Canon EOS 80D + 18-55mm
          v-card-text.subtitle-1
            v-icon mdi-account-cog
            span Hana Lysáková
          v-card-actions
            v-btn Rezervovat
            v-btn(@click="dialog = true", text)
              v-icon(left) mdi-calendar
              | Kalendář

      v-data-table.elevation-1(
        key="2",
        v-else,
        fixed-header,
        height="calc(100vh - 90px)",
        disable-pagination,
        hide-default-footer,
        v-model="selected",
        :headers="headers",
        :items="desserts",
        item-key="name",
        show-select
      )
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
            v-btn(icon, v-if="!resourceDialogEditing" @click="editResource")
              v-icon mdi-pencil
            v-btn(icon, title="Uložit úpravy" v-else-if="resourceDialogEditing && activeResource.id" @click="saveResource")
              v-icon mdi-content-save
            v-btn(icon, title="Vytvořit zdroj"  v-else @click="saveResource")
              v-icon mdi-plus-circle
            v-btn(icon, @click="resourceDialog = false")
              v-icon mdi-close
          v-card-text
            v-row
              v-col(style="max-width: 340px")
                v-img.rounded(width="300", src="https://picsum.photos/300/250")
              v-col
                v-form#resource-form
                  v-text-field(v-model="activeResource.name", hide-details, label="Název",prepend-icon="mdi-form-textbox", :disabled="!resourceDialogEditing")
                  v-select(prepend-icon="mdi-account-cog",
                    v-model="activeResource.provider"
                    hide-details,
                    :disabled="!resourceDialogEditing",
                    label="Výdejář",
                    :items="['Hana Lysáková']")
                  v-select.mt-2(prepend-icon="mdi-shield-lock", :disabled="!resourceDialogEditing", value="LEMMA nad 100" label="Úroveň oprávnění" :items="['LEMMA nad 100']")
                  v-autocomplete(v-model="activeResource.tags",prepend-icon="mdi-tag", class="mt-0 pt-0", :items="tags", :disabled="!resourceDialogEditing", chips, deletable-chips, small-chips, label="Štítky", multiple)
                    template(v-slot:append-item)
                      v-divider
                      v-text-field.px-3(v-model="newTag", label="Nový štítek")
                        template(slot="append")
                          v-btn(icon, @click="createTag")
                            v-icon mdi-plus
                  v-text-field(v-model="activeResource.price", label="Cena",prepend-icon="mdi-cash-multiple", type="number", :disabled="!resourceDialogEditing")
                    template(slot="append") Kč
            v-row
              v-col
                h2 Popis
                div(v-if="!resourceDialogEditing" v-html="activeResource.description")
                v-textarea(v-else, v-model="activeResource.description")
              v-col
                h2 Interní poznámky
                div(v-if="!resourceDialogEditing" v-html="activeResource.internalNotes")
                v-textarea(v-else, v-model="activeResource.internalNotes")
    portal(to='add-resource-btn')
        v-btn.mb-3(color="primary", block @click="createResource") Přidat zdroj
</template>

<script>
import API from "@/model/httpclient";


const emptyResource = () => {
  return {
    name: "",
    description: "",
    internalNotes: "",
    price: 0,
    image: null,
    tags: [],
    provider: null,
    requiredPermissionLevel: 0
  };
};

export default {
  props: ["displayStyle"],
  mounted() {
    this.loadTags();
    this.loadProviders();

  },
  computed: {
    month() {
      console.log(
          new Date(this.value).toLocaleString("cs-CZ", {month: "long"})
      );
      return new Date(this.value).toLocaleString("cs-CZ", {month: "long"});
    },
  },
  methods: {
    click(props) {
      console.log(props);
    },
    createResource() {
      this.activeResource = emptyResource()
      this.resourceDialog = true
    },
    openResource(resource) {
    },
    editResource() {
      this.resourceDialogEditing = true;
    },
    saveResource() {
      this.resourceDialogEditing = false;
    },
    async loadTags() {
      this.tags = await API.getTags()
    },
    async loadProviders() {
      this.providers = API.getUsers('PROVIDER')
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
      tags: [],
      newTag: '',
      providers: [],
      selected: [],
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
      resourceDialog: true,
      resourceDialogEditing: true,
      activeResource: emptyResource(),
      headers: [
        {
          text: "Dessert (100g serving)",
          align: "start",
          sortable: false,
          value: "name",
        },
        {text: "Calories", value: "calories"},
        {text: "Fat (g)", value: "fat"},
        {text: "Carbs (g)", value: "carbs"},
        {text: "Protein (g)", value: "protein"},
        {text: "Iron (%)", value: "iron"},
      ],
      desserts: [
        {
          name: "Frozen Yogurt",
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: "1%",
        },
        {
          name: "Ice cream sandwich",
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3,
          iron: "1%",
        },
        {
          name: "Eclair",
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0,
          iron: "7%",
        },
        {
          name: "Cupcake",
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3,
          iron: "8%",
        },
        {
          name: "Gingerbread",
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9,
          iron: "16%",
        },
        {
          name: "Jelly bean",
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0,
          iron: "0%",
        },
        {
          name: "Lollipop",
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0,
          iron: "2%",
        },
        {
          name: "Honeycomb",
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5,
          iron: "45%",
        },
        {
          name: "Donut",
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9,
          iron: "22%",
        },
        {
          name: "KitKat",
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7,
          iron: "6%",
        },
      ],
    };
  },
};
</script>

<style lang="scss">
#resource-form{
  .v-label--is-disabled,.v-select__selection--disabled,.theme--dark.v-input--is-disabled, .v-icon--disabled, .theme--dark.v-input--is-disabled input, .v-chip__content {
    color: white !important;
  }
  .v-input--is-disabled.v-select .v-input__append-inner {
    display: none;
  }
  .v-chip--disabled{
    opacity: 1;
  }

}

#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-gap: 16px;
  justify-content: center;
  width: 100%;
}
</style>
