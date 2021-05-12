import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import cs from 'vuetify/es5/locale/cs';

Vue.use(Vuetify);

export default new Vuetify({
  // breakpoint: {
  //   thresholds: {
  //     xs: 340,
  //     sm: 1540,
  //     md: 1600,
  //     lg: 1700,
  //   },
  // },
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
