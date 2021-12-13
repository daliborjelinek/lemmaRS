<template>
  <v-main>
    <v-container>
      <v-card>
        <v-tabs v-model="tab">
          <v-tab> Moje projekty</v-tab>
          <v-tab> Všechny projekty</v-tab>
          <v-tab> Skupiny projektů</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <!--MY PROJECTS-->
          <v-tab-item>
            <projects-table :projects.sync="myProjects" :headers="myProjectHeaders" :project-groups="projectGroups"/>
          </v-tab-item>
          <!--ALL PROJECTS-->
          <v-tab-item>
            <projects-table :projects.sync="projects" :headers="allProjectHeaders" :project-groups="projectGroups"/>
          </v-tab-item>
          <!--PROJECT GROUP-->
          <v-tab-item>
              <ProjectGroups :project-groups.sync="projectGroups"/>
          </v-tab-item>
        </v-tabs-items>
      </v-card>

    </v-container>
  </v-main>
</template>

<script>
import API from "@/model/httpclient";
import ProjectGroups from "@/views/projects/ProjectGroupsTable"
import ProjectsTable from "@/views/projects/ProjectsTable";


export default {
  components: {ProjectsTable, ProjectGroups},
  data: () => ({
    tab: null,
    allProjectHeaders: [
      {text: "Jméno", value: "name"},
      {text: "Vytvořeno", value: "created_at"},
      {text: "Dokončeno", value: "finished"},
      {text: "Vlastník", value: "owner"},
      {text: "Skupina", value: "group"},

    ],
    myProjectHeaders: [
      {text: "Jméno", value: "name"},
      {text: "Vytvořeno", value: "created_at"},
      {text: "Dokončeno", value: "finished"},
      {text: "Skupina", value: "group"},
      {text: "Akce", value: "actions", sortable: false},
    ],
    projectGroups: [],
    loadingProjects: false,
  }),
  computed: {
    projects(){
      return this.$store.state.projects
    },
    myProjects(){
      return this.$store.getters.myProjects
    }
  },

  watch: {},

  async created() {
    await this.$store.dispatch('getProjects')
    this.projectGroups = await API.getProjectGroups();
  },

  methods: {


  },
};
</script>
