<template>
     <v-card elevation="5" class="fill-height d-flex flex-column" rounded="0">
        <v-card-title>
          Nová rezervace <v-spacer />
          <v-btn icon><v-icon>mdi-delete</v-icon> </v-btn></v-card-title
        >
        <v-card-text class="flex-grow-1 d-flex flex-column">
          <div>
            <v-alert
            
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
                  label="Termín rezervace"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker v-model="date" no-title range scrollable>
                <v-spacer></v-spacer>
                <v-btn text color="primary" @click="modal = false">
                  Cancel
                </v-btn>
                <v-btn text color="primary" @click="$refs.dialog.save(date)">
                  OK
                </v-btn>
              </v-date-picker>
            </v-dialog>
            <v-autocomplete
              :items="[]"
              :loading="false"
              color="white"
              hide-no-data
              hide-selected
              item-text="Description"
              item-value="API"
              label="Projekt"
              placeholder="Název projektu"
              prepend-icon="mdi-database-search"
              return-object
            ></v-autocomplete>
          </div>

          <v-list-item-group
            class="flex-grow-1"
            style="height: 200px; overflow-y: auto"
          >
            <v-list-item dense v-for="(item, i) in 15" :key="i">
              <v-list-item-content>
                <v-list-item-title>Canon 550D + 18 - 55mm</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn x-small icon>
                  <v-icon color="grey lighten-1">mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list-item-group>
        </v-card-text>
      </v-card>
</template>

<script>
export default {
  data: () => ({
    date: ["2019-09-10", "2019-09-20"],
    showCalendar: false
  }),
  computed: {
    dateRangeText() {
      return this.date.join(" ~ ");
    },
  },
};
</script>