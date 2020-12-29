import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import cs from 'vuetify/es5/locale/cs';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
      light: {
        primary: '#0000dc',

        accent: '#FFC107',

      },
      dark: {
        primary: '#3f51b5',
      },
    },
    dark: true
  },
  lang: {
    locales: { cs },
    current: 'cs',
  },
  icons: {
    iconfont: 'mdi',
  }
});
