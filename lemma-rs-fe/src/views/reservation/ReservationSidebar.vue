<template>
     <v-card elevation="5" color="#1e1e1ee6" class="fill-height d-flex flex-column" rounded="0">
        <v-card-title>
          Rezervace <v-spacer />
          <v-btn disabled color="primary" >odeslat </v-btn></v-card-title
        >
        <v-card-text class="flex-grow-1 d-flex flex-column">
          <div>
            <v-alert
              class="mb-0"
              dense
              icon="mdi-alert"
              text
              type="warning"
            >Vyžadováno schválení</v-alert>


            <v-dialog
              ref="dialog"
              v-model="showCalendar"
              :return-value.sync="date"
              persistent
              width="290px"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="dateRangeText"
                  hide-details
                  label="Termín rezervace"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker format="24hr" v-model="date" :min="new Date().toISOString()" no-title range scrollable>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="modal = false">
                  Cancel
                </v-btn>
                <v-btn text color="primary" @click="$refs.dialog.save(date)">
                  OK
                </v-btn>
              </v-date-picker>
            </v-dialog>
            <div class="d-flex">
              <Timepicker icon="true" class="pr-2" label="Začatek"/><Timepicker label="Konec"/>
            </div>
            <v-autocomplete
              :items="[]"
              :loading="false"
              color="white"
              hide-selected
              hide-details
              item-text="Description"
              item-value="API"
              label="Projekt"
              prepend-icon="mdi-database-search"
              return-object
            ></v-autocomplete>
          </div>

          <v-list-item-group
            class="flex-grow-1"
            style="height: 200px; overflow-y: auto"
          >
            <v-list-item dense v-for="(resource, i) in selectedResources" :key="resource.id">
              <v-list-item-content>
                <v-list-item-title>{{resource.name}}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn @click="removeResource(resource)" x-small icon>
                  <v-icon small color="grey lighten-1">mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list-item-group>
        </v-card-text>
      </v-card>
</template>

<script>
import Timepicker from "@/components/Timepicker";
export default {
  components: {Timepicker},
  data: () => ({
    date: [],
    showCalendar: false
  }),
  computed: {
    dateRangeText() {
      return this.date.join(" ~ ");
    },
    selectedResources() {
      return this.$store.state.reservation.selectedResources
    }
  },
  methods: {
    removeResource(res) {
      this.$store.commit('removeSelectedItem',res)
    }
  }
};
</script>
