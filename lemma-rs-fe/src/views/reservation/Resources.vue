<template>
     <div
        class="flex-grow-1 pa-3"
        style="height: 0; overflow-y: auto"
        color="primary"
      >
      <transition mode="out-in" name="fade">
        <div key=1 v-if="displayStyle === 'cards'" id="grid">
          <v-card :key="index" v-for="(item, index) in 20" max-width="300">
            <v-img
              height="200"
              :src="'https://picsum.photos/300/250?random=' + index"
            ></v-img>

            <v-card-title>Canon EOS 80D + 18-55mm</v-card-title>
            <v-card-text> </v-card-text>
            <v-card-actions>
              <v-btn > Rezervovat </v-btn>
              <v-btn text> <v-icon left v-text="'mdi-calendar'" /> kalendář </v-btn>
            </v-card-actions>
          </v-card>
        </div>
          <v-data-table
          key="2"
          v-else
          fixed-header
          height="calc(100vh - 90px)"
          disable-pagination
          hide-default-footer
    v-model="selected"
    :headers="headers"
    :items="desserts"
    item-key="name"
    show-select

    class="elevation-1"
  >
  

  </v-data-table>
  </transition>
      </div>
</template>

<script>
  export default {
      props:['displayStyle'],
      methods:{
          click(props){
              console.log(props)
          }
      },
    data () {
      return {
        selected: [],
        headers: [
          {
            text: 'Dessert (100g serving)',
            align: 'start',
            sortable: false,
            value: 'name',
          },
          { text: 'Calories', value: 'calories' },
          { text: 'Fat (g)', value: 'fat' },
          { text: 'Carbs (g)', value: 'carbs' },
          { text: 'Protein (g)', value: 'protein' },
          { text: 'Iron (%)', value: 'iron' },
        ],
        desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            iron: '1%',
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            iron: '1%',
          },
          {
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            iron: '7%',
          },
          {
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            iron: '8%',
          },
          {
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            iron: '16%',
          },
          {
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            iron: '0%',
          },
          {
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            iron: '2%',
          },
          {
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            iron: '45%',
          },
          {
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            iron: '22%',
          },
          {
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            iron: '6%',
          },
        ],
      }
    },
  }
</script>

<style scoped>
#grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 300px);
  grid-gap: 16px;
  justify-content: center;
  width: 100%;
}
</style>