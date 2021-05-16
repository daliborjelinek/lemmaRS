<template>
  <v-dialog
      v-model="modal"
      width="290px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
          :class="icon? 'mr-1' : 'ml-1'"
          v-model="time"
          :rules="[(v) => !!v || 'Vyplňte čas rezervace']"
          :label="label"
          readonly
          :prepend-icon="icon ? 'mdi-alarm-multiple' : ''"
          v-bind="attrs"
          v-on="on"
      ></v-text-field>
    </template>
    <v-time-picker
        v-if="modal"
        :allowed-hours="allowedHours"
        v-model="time"
        @change="change"
        format="24hr"
        full-width
    >
      <v-spacer></v-spacer>
      <v-btn
          text
          color="primary"
          @click="modal = false"
      >
        Ok
      </v-btn>
    </v-time-picker>
  </v-dialog>
</template>

<script>
export default {
  props:['label','icon', 'value'],
  name: "Timepicker",
  data: function () {
    return {
      modal: false,
      time: null,
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(newVal, oldVal) {
        this.time = newVal
      }
    }
  },
  methods:{
    change(val){
      console.log(val)
      this.$emit('change',val)
    },
    allowedHours(h){
        return (h > 8) && (h < 15)
    }
  }

}
</script>

<style scoped>

</style>
