<template>
  <v-dialog v-model="projectDialog" max-width="900" >
    <v-card>
      <v-toolbar color="primary" dark>{{ activeProject.id ? 'Projekt - '+ activeProject.name : 'Nový projekt' }}</v-toolbar>

      <v-card-text class="secondary darken-2">
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <v-sheet elevation="2" rounded class="pa-2">
              <v-form ref="projectForm" lazy-validation>
                <v-text-field
                    v-model="activeProject.name"
                    :rules="[(v) => !!v || 'Vyplňte jméno projektu']"
                    label="Jméno"
                    prepend-icon="mdi-form-textbox"
                />

                <v-autocomplete
                    v-model="activeProject.group"
                    :items="projectGroups"
                    :rules="[(v) => !!v || 'Vyplňte jméno projektu']"
                    :item-text="item => item.name"
                    :item-value="item => item.id"
                    label="Skupina"
                    prepend-icon="mdi-account-group"
                />
                <v-textarea
                    prepend-icon="mdi-note-text-outline"
                    v-model="activeProject.description"
                    label="Popis"
                />

                <v-checkbox
                    v-if="activeProject.id"
                    prepend-icon="mdi-check-all"
                    v-model="activeProject.finished"
                    label="Projekt je dokončen"
                ></v-checkbox>

              </v-form>
            </v-sheet>
          </v-col>
          <v-col>
            <v-sheet elevation="2" rounded class="pa-2 ">
              <v-subheader

              >
                Členové
              </v-subheader>

              <div class="pa-3 text-center" v-if="!activeProject.id">
                Členy lze přidat až po vytvoření projektu
              </div>
              <v-list  v-else>
                <v-list-item
                    v-for="member in activeProject.members"
                    :key=member.id
                >
                  <v-list-item-icon>
                    <v-icon>mdi-account</v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title v-text="member.fullname"></v-list-item-title>
                  </v-list-item-content>

                  <v-list-item-avatar>
                    <v-btn
                        @click="removeProjectMember(member.id)"
                        fab
                        x-small
                        dark
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-avatar>
                </v-list-item>
                <v-divider

                />
                <v-list-item>
                  <v-list-item-icon class="align-self-center">
                    <v-icon>mdi-account</v-icon>
                  </v-list-item-icon>

                  <v-list-item-content>
                    <v-list-item-title>
                      <v-autocomplete
                          :disabled="!activeProject.id"
                          v-model="selectedMember"
                          :items="users"
                          :item-text="item => item.fullname"
                          :item-value="item => item.id"
                          :hint="!activeProject.id ? 'Členy lze přidávat až po vytvoření projektu' : ''"
                          label="Nový člen"
                      >
                      </v-autocomplete>
                    </v-list-item-title>
                  </v-list-item-content>

                  <v-list-item-avatar>
                    <v-btn
                        :disabled="!activeProject.id || !selectedMember"
                        color='success'
                        @click="addProjectMember"
                        fab
                        x-small
                        dark
                    >
                      <v-icon>mdi-plus-circle</v-icon>
                    </v-btn>
                  </v-list-item-avatar>
                </v-list-item>
              </v-list>
            </v-sheet>
          </v-col>
        </v-row>


      </v-card-text>

      <v-card-actions>
        <v-spacer/>
        <v-btn text @click="projectDialog = false"> Zavřít</v-btn>
        <v-btn text @click="saveProject"> {{activeProject.id ? 'Uložit' : 'Vytvořit'}}</v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import API from "@/model/httpclient";

const emptyProject = () => {
  return {
    name: "",
    description: "",
    active: true,

  };

};
export default {
  name: "ProjectEditorModal",
  async created() {
    this.users = await API.getUsers()
    this.projectGroups = await API.getProjectGroups();
  },
  computed:{
    projects(){
      return this.$store.state.projects
    },
  },
  data: () => ({
    projectGroups: [],
    projectDialog: false,
    activeProject: emptyProject(),
    selectedMember: null,
    users: [],
  }),
  methods:{
    openCreateDialog() {
      this.activeProject = emptyProject()
      if (this.$refs.projectForm) this.$refs.projectForm.resetValidation()
      this.projectDialog = true
    },
    editProject(project) {
      this.activeProject = JSON.parse(JSON.stringify(project))
      this.projectDialog = true
    },
    reloadActiveProject(projectId = null){
      const id = projectId || this.activeProject.id
      this.$nextTick(() => {
        this.activeProject = this.projects.find(project => project.id === id)
      });
    },
    async createProject() {
      try {
        const newProject = await API.createProject(this.activeProject);
        await this.$store.dispatch('getProjects')
        console.log(newProject)
        this.reloadActiveProject(newProject.id)
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Projekt vytvořen",
        });
      } catch (e) {
        console.log(e);
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládáni selhalo",
        });
      }

    },
    async updateProject() {
      try {
        await API.updateProject(this.activeProject)
        await this.$store.dispatch('getProjects')
        this.projectDialog = false;
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Projekt uložen",
        });

      } catch (e) {
        console.log(e)
        await this.$store.dispatch("notify", {
          type: "error",
          text: "Ukládání selhalo",
        });
      }
    },
    async saveProject() {
      if (!this.$refs.projectForm.validate()) return;
      if (!this.activeProject.id) {
        await this.createProject()
      } else {
        await this.updateProject()
      }
    },
    async addProjectMember() {
      try{
        await API.addProjectMember(this.activeProject.id, this.selectedMember)
        await this.$store.dispatch('getProjects')
        this.reloadActiveProject()
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Člen projektu přiřazen",
        });
      } catch (e){
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Ukládání se nezdařilo",
        });
      }

    },
    async removeProjectMember(memberId){
      try{
        await API.removeProjectMember(this.activeProject.id, memberId)
        await this.$store.dispatch('getProjects')
        this.reloadActiveProject()
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Člen projektu odebrán",
        });
      } catch (e){
        await this.$store.dispatch("notify", {
          type: "success",
          text: "Ukládání se nezdařilo",
        });
      }

    }
  }
}
</script>

<style scoped>

</style>
