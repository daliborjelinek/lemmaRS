<template>
  <div>
    <v-data-table
        :headers="headers"
        :items="projects"
        :search="search"
        :items-per-page="5"
        class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-text-field
              style="max-width: 300px"
              v-model="search"
              append-icon="mdi-magnify"
              label="Hledat"
              single-line
              hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click.stop="openCreateDialog">
            Vytvořit projekt
          </v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.finished="{ item }">
        <v-icon>
          {{ item.finished ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}
        </v-icon>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editProject(item)">
          mdi-pencil
        </v-icon>
      </template>
      <template v-slot:item.created_at="{ item }">
        {{ $moment(item.created_at).locale("cs").format('LLL') }}
      </template>
      <template v-slot:item.owner="{ item }">
        {{ item.owner.fullname }}
      </template>
      <template v-slot:item.group="{ item }">
        {{ getGroupNameById(item.group) }}
      </template>
    </v-data-table>

    <ProjectEditorModal ref="projectEditorModal"/>
  </div>
</template>

<script>
import ProjectEditorModal from "@/views/projects/ProjectEditorModal";
const emptyProject = () => {
  return {
    name: "",
    description: "",
    active: true,
  };
};
export default {
  name: "ProjectsTable",
  props: ['headers', 'projects', 'projectGroups'],
  data: () => ({
    search: "",
    loadingProjects: false,
  }),
  computed: {},
  components:{
    ProjectEditorModal
  },
  methods: {
    getGroupNameById(id) {
      return this.projectGroups.find(group => group.id === id)?.name
    },
    openCreateDialog() {
      this.$refs.projectEditorModal.openCreateDialog()
    },
    editProject(project) {
      this.$refs.projectEditorModal.editProject(project)
    },
  },
}
</script>

<style scoped>

</style>
