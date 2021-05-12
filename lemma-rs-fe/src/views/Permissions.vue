<template>
  <v-main>
    <v-container>
      <v-card>
        <v-tabs v-model="tab">
          <v-tab> Moje oprávnění</v-tab>
          <v-tab> Ke schválení</v-tab>
          <v-tab> Všechny</v-tab>
        </v-tabs>
       dadwa
      </v-card>

    </v-container>
  </v-main>
</template>

<script>
export default {
  name: "Permissions",
  data: function () {
    return {
      tab:0
    }
  }
}
</script>

<style scoped>

</style>
