<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col>
          <v-sheet
            class="mx-auto pa-3"
            elevation="3"
            rounded="lg"
            max-width="500px"
          >
            <div class="d-flex  justify-space-between">
              <h1>{{ $store.state.user.profile.fullname }}</h1>
              <v-chip class="ma-2">
                {{ currentUserRole }}
              </v-chip>
            </div>

            <v-form>
              <v-select
                v-if="currentUserRole !== 'COMMON'"
                v-model="role_display"
                :items="role"
                label="Zobrazit GUI jako"
              ></v-select>

              <v-text-field
                v-model="email"
                label="E-mail"
                required
              ></v-text-field>

              <v-text-field label="Telefon" v-model="phone"></v-text-field>
              
              <v-text-field label="Místnost" v-model="phone"></v-text-field>

              <v-textarea
                name="Adresa"
                label="Adresa"
                v-model="address"
                hint="Adresa"
              ></v-textarea>

              <v-spacer />
              <v-btn color="primary" class="mt-3 ml-auto" @click="save">
                Uložit
              </v-btn>
            </v-form>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
<script>
import { createHelpers } from "vuex-map-fields";
import { USER_UPDATE } from "@/store/actions/user";
const { mapFields } = createHelpers({
  getterType: "getUserField",
  mutationType: "updateUserField",
});
export default {
  data: () => ({}),
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
        { text: "Běžný  uživatel", value: "COMMON" },
        { text: "Výdejář", value: "PROVIDER" },
      ];
    },
  },
  methods: {
    save() {
      this.$store.dispatch(USER_UPDATE);
    },
  },
};
</script>
