<template>
  <div>
    <v-snackbar
      :style="calcPadding(index)"
      v-for="(toast, index) in toasts"
      :key="toast.id"
      right
      v-model="toast.open"
      class="error--text"
     
      :timeout="-1"
    >
      <v-icon  :color="getColor(toast.type)"> {{getIcon(toast.type)}} </v-icon> {{ toast.text }}

      <template v-slot:action>
        <v-btn :color="getColor(toast.type)" text @click="hideNotification(toast.id)"> Close </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>
<script>
export default {
  computed: {
    toasts() {
      return this.$store.state.toasts;
    },
  },
  methods: {
    calcPadding(index) {
      return {
        "padding-bottom":
          this.toasts.filter((toast) => toast.open && toast.id < index).length *
            60 +
          "px",
      };
    },
    getIcon(type){
        if(type === 'error') return 'mdi-alert-octagon'
        else if (type === 'success') return 'mdi-check-circle-outline'
        else return 'mdi-information-outline'

    },
    getColor(type){
         if(type === 'error') return 'error'
        else if (type === 'success') return 'success'
        else return ''

    },
    hideNotification(id){
        this.$store.commit('hideNotification',id)
    }
  },
};
</script>