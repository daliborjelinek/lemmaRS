<template lang="pug">
  v-select(
    v-bind="$attrs"
    v-on="$listeners"
    v-model="dataValue"
    :items="items")
</template>

<script>
import API from '@/model/httpclient'

export default {
  name: "ApiSelect",
  props: {
    value:{
      type: [Number, String]
    }
    ,
    query: {
      type: String
    },
    defaultIndex: {
      type: Number,
      default: 0
    }
  },
  watch: {
    value: {
      immediate: true,
      handler: function(newValue) {
        this.dataValue = newValue
      }
    }
  },
  data: function () {
    return {
      items: [],
      dataValue: this.value,
    }
  },
  async mounted() {
    await this.getItems()
  },
  methods: {
    async getItems() {
      this.items = await API.commonGetRequest(this.query)
      this.dataValue = this.items.length > 0 ? this.items[this.defaultIndex] : []
      this.$emit('input',this.dataValue.id)

    }
  }
}
</script>

<style scoped>

</style>
