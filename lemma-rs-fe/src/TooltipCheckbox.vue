<template>
<div>
  <v-tooltip open-delay="500" right >
    <template v-slot:activator="{ on }">
      <div v-on="on">
      <v-checkbox
        class="mt-0"
        @change="click"
        hide-details
        :input-value="value"
        :disabled="disabled"
      >
        <template v-slot:label>
          <span >{{ label }} </span>
        </template>
      </v-checkbox>
      </div>
    </template>
    {{ tooltip }}
  </v-tooltip>
  </div>
</template>

<script>
export default {
  props: ["value", "tooltip", "label", "disabled"],
  methods: {
    click(e) {
      this.$emit("input", e);
    },
  },
};
</script>