<template>
  <div>
    <v-data-table
        :headers="projectGroupHeaders()"
        :items="projectGroups"
        :items-per-page="5"
        :search="search"
        class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              hide-details
              label="Hledat"
              single-line
              style="max-width: 300px"
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn
              v-if="$store.getters.getDisplayRole === 'ADMIN'"
              color="primary"
              @click.stop="openCreateDialog"
          >
            Vytvořit skupinu
          </v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.active="{ item }">
        <v-icon>
          {{ item.active ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}
        </v-icon>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon class="mr-2" small @click="editProjectGroup(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteProjectGroup(item)"> mdi-delete</v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="projectGroupDialog" max-width="500">
      <v-card>
        <v-card-title class="headline"> {{ activeGroup.id ? activeGroup.name : 'Nová skupina' }}</v-card-title>

        <v-card-text>
          <v-form ref="projectGroupForm" lazy-validation>
            <v-text-field
                v-model="activeGroup.name"
                :rules="[(v) => !!v || 'Vyplňte jméno skupiny']"
                label="Jméno"
            ></v-text-field>
            <v-text-field
                v-model="activeGroup.description"
                label="Popis"
            ></v-text-field>
            <v-checkbox
                v-model="activeGroup.active"
                label="Aktivní (viditelná při vytváření nových projektů)"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer/>
          <v-btn text @click="projectGroupDialog = false"> Zavřít</v-btn>
          <v-btn text @click="saveProjectGroup"> {{ activeGroup.id ? 'Uložit' : 'Vytvořit' }}</v-btn>

        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import API from "@/model/httpclient";
import ProjectGroups from "@/views/projects/ProjectGroupsTable"

const emptyGroup = () => {
  return {
    name: "",
    description: "",
    active: true,
  };
};
export default {
  components: {ProjectGroups},
  props: ['projectGroups'],
  data: () => ({
    search: "",
    activeGroup: emptyGroup(),
    projectGroupDialog: false,
    loadingProjectsGroups: false,
  }),

  computed: {},

  watch: {},

  methods: {
    projectGroupHeaders() {
      const headers = [
        {text: "Jméno", value: "name"},
        {text: "Popis", value: "description"},
        {text: "Aktivní", value: "active"},
        {text: "Akce", value: "actions", sortable: false},
      ]
      if (this.$store.getters.getDisplayRole === 'COMMON')
        headers.pop()
      return headers
    },
    openCreateDialog() {
      this.activeGroup = emptyGroup()
      if (this.$refs.projectGroupForm) this.$refs.projectGroupForm.resetValidation()
      this.projectGroupDialog = true
    },
    editProjectGroup(group) {
      this.activeGroup = {...group}
      this.projectGroupDialog = true
    },
    async createProjectGroup() {
      try {
        await API.createProjectGroup(this.activeGroup);
        this.$emit('update:projectGroups', await API.getProjectGroups())
        this.projectGroupDialog = false;
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Skupina vytvořena",
        });
      } catch (e) {
        console.log(e);
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládáni selhalo",
        });
      }

    },
    async updateProjectGroup() {
      try {
        await API.updateProjectGroup(this.activeGroup)
        this.$emit('update:projectGroups', await API.getProjectGroups())
        this.projectGroupDialog = false;
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Skupina uložena",
        });

      } catch (e) {
        console.log(e)
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládání skupiny selhalo",
        });
      }
    },
    async saveProjectGroup() {
      if (!this.$refs.projectGroupForm.validate()) return;
      if (!this.activeGroup.id) {
        await this.createProjectGroup()
      } else {
        await this.updateProjectGroup()
      }
    },
    async deleteProjectGroup(group) {
      if (confirm('Opravdu chcete smazat tuto skupinu?')) {
        try {
          await API.deleteProjectGroup(group)
          this.$emit('update:projectGroups', await API.getProjectGroups())
          await this.$store.dispatch("notify", {
            type: "success",
            text: "Skupina odstraněna",
          });
        } catch (e) {
          console.log(e)
          await this.$store.dispatch("notify", {
            type: "error",
            text: "Odstranění skupiny selhalo",
          });
        }

      }
    }
  },
};
</script>

<style scoped>

</style>
