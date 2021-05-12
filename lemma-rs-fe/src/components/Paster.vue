<template>
  <v-dialog
      :value="enable"
      max-width="290"
      @input="close"
  >
    <v-card>
      <div class="pa-3">
        Stiskněte ctrl+v pro vložení obrázku
      </div>



    </v-card>
  </v-dialog>

</template>

<script>
export default {
  name: "Paster.vue",
  props:['enable'],
  methods: {
    close(){
      this.$emit('close',[])
    },
    handlePaste(e){
      if(this.enable){
        this.$emit('close',e.clipboardData.files)
      }

    }
  },
  created: function() {
    window.addEventListener('paste', this.handlePaste);

  },
  destroyed: function() {
    window.removeEventListener('paste', this.handlePaste);
  }
}
</script>

<style scoped>

</style>
