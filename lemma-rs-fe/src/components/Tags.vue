<template>
  <span>
    <v-chip
        v-for="tag in tags"
        class="ma-2"
        small
        :color="getColor(tag)"
    >
      {{tag}}
    </v-chip>
  </span>

</template>

<script>

export default {
  props: ['tags'],
  name: "Tags.vue",
  methods:{
    getColor(name){
      switch (name){
        case 'audio': return '#1a237e'
        case 'video': return '#311b92'
        case 'objektivy': return '#4a148c'
        case 'světla': return '#1b5e20'
        case 'stabilizace': return '#004d40'
        case 'příslušenství': return '#01579b'
        default: return 'secondary'
          // code block
      }
    }
  }
}
</script>

<style scoped>

</style>
