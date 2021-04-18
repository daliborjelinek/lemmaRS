<template>
  <div
      class="flex-grow-1 pa-3"
      style="height: 0; overflow-y: auto"
      color="primary"
  >
    <transition mode="out-in" name="fade">
      <div key="1" v-if="displayStyle === 'cards'" id="grid">
        <v-card @click="openResource(item)" v-ripple class="pointer" :key="index" v-for="(item, index) in 20"
                max-width="300">
          <v-img
              height="200"
              :src="'https://picsum.photos/300/250?random=' + index"
          ></v-img>

          <v-card-title>Canon EOS 80D + 18-55mm</v-card-title>
          <v-card-text>
            <div class="subtitle-1">
              <v-icon>mdi-account-cog</v-icon>
              Hana Lysáková
            </div>

          </v-card-text>
          <v-card-actions>
            <v-btn> Rezervovat</v-btn>
            <v-btn @click="dialog = true" text>
              <v-icon left v-text="'mdi-calendar'"/>
              kalendář
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
      <v-data-table
          key="2"
          v-else
          fixed-header
          height="calc(100vh - 90px)"
          disable-pagination
          hide-default-footer
          v-model="selected"
          :headers="headers"
          :items="desserts"
          item-key="name"
          show-select
          class="elevation-1"
      >
      </v-data-table>
    </transition>
    <v-dialog v-model="dialog">
      <v-card>
        <v-toolbar color="primary" dark>
          Canon EOD 500D
          <v-btn
              icon
              class="ma-2"
              @click="
              $refs.calendar.prev();
              click($refs.calendar);
            "
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          {{ month }}
          <v-btn icon class="ma-2" @click="$refs.calendar.next()">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
          <v-spacer/>
          <v-btn
              icon
              dark
              @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>

        </v-toolbar
        >


        <v-sheet class="pa-2" height="400">
          <v-calendar
              v-model="value"
              ref="calendar"
              color="primary"
              :events="events"
              event-color="cyan"
              type="month"
          ></v-calendar>
        </v-sheet>


      </v-card>
    </v-dialog>
    <v-dialog
        v-model="resourceDialog"
        max-width="900"
    >
      <template v-slot:default="dialog">
        <v-card>
          <v-toolbar
              color="primary"
              dark
          >Canon eos 500D
            <v-spacer/>
            <v-btn
                icon
                dark
            >
              <v-icon small>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
                icon
                dark
                @click="resourceDialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>

          </v-toolbar>
          <v-card-text>
            <v-row>
              <v-col>
                <v-img class="rounded"
                       width="300"
                       src="https://picsum.photos/300/250"
                ></v-img>
              </v-col>
              <v-col>
                <div class="subtitle-1">
                  <v-icon>mdi-account-cog</v-icon>
                  Hana Lysáková
                </div>
                <div class="my-2">
                  <v-icon class="mr-1">
                    mdi-tag
                  </v-icon>
                  <v-chip
                      class="mr-2"
                      small
                      color="pink"
                      label
                      text-color="white"
                  >
                    <v-icon small left>
                      mdi-label
                    </v-icon>
                    Audio
                  </v-chip>
                </div>
                <v-btn color="primary">
                  Rezervovat
                </v-btn>
                <v-btn @click="dialog = true" text>
                  <v-icon left v-text="'mdi-calendar'"/>
                  kalendář
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <h2>Popis </h2>

                <div>
                  Nějaký interní popis
                </div>
              </v-col>
              <v-col>
                <h2>Interní poznámky</h2>
                <div>
                  Nějaké interní poznámky
                </div>
              </v-col>
            </v-row>

          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn
                text
                @click="dialog.value = false"
            >Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>

  </div>
</template>

<script>
export default {
  props: ["displayStyle"],
  computed: {
    month() {
      console.log(new Date(this.value).toLocaleString('cs-CZ', {month: 'long'}),)
      return new Date(this.value).toLocaleString('cs-CZ', {month: 'long'})
    },
  },
  methods: {
    click(props) {
      console.log(props);
    },
    openResource(resource) {

    }
  },
  data() {
    return {
      value: new Date(),
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

<style scoped>
#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-gap: 16px;
  justify-content: center;
  width: 100%;
}
</style>
