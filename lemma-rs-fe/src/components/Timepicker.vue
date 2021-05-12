<template>
  <v-dialog
      ref="dialog"
      v-model="modal"
      :return-value.sync="time"
      persistent
      width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
          :class="icon? 'mr-1' : 'ml-1'"
          v-model="time"
          @change="(value) => $emit('change',value)"
          :label="label"
          readonly
          :prepend-icon="icon ? 'mdi-alarm-multiple' : ''"
          hide-details
          v-bind="attrs"
          v-on="on"
      ></v-text-field>
    </template>
    <v-time-picker
        v-if="modal"
        v-model="time"
        full-width
    >
      <v-spacer></v-spacer>
      <v-btn
          text
          color="primary"
          @click="modal = false"
      >
        Cancel
      </v-btn>
      <v-btn
          text
          color="primary"
          @click="$refs.dialog.save(time)"
      >
        OK
      </v-btn>
    </v-time-picker>
  </v-dialog>
</template>

<script>
export default {
  props:['label','icon'],
  name: "Timepicker",
  data: function (){
    return {
      modal: false,
      time: null,
    }
  }
}
</script>

<style scoped>

</style>
