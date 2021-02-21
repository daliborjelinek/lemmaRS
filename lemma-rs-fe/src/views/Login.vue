<template>
  <v-main>
    <div id="login">
      <v-card>
        <v-card-text class="pt-4 text-center elevation-3">
          <div>
            <img height="50px" class="p-3" src="../assets/lemma.png" /><br />

            <p class="display-1">RS lemma</p>
            <div @click="login()" class="munibtn" v-ripple></div>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </v-main>
</template>

><script>
import axios from 'axios'
export default {
  methods: {
    login() {
         const url =
        "https://oidc.muni.cz/oidc/authorize?client_id=68a86438-6400-4b77-8a4a-d6b3a52ac6b6&redirect_uri=http://localhost:8080/auth/signinwin/main&scope=openid profile email&response_type=token id_token&response_mode=form_post";
         const newwindow = window.open(url, "popup", "height=600,width=500");
    },
    authCallback(event) {
       // console.log('callback', 'http://localhost:8080', event.origin)
      if (event.origin !== 'http://localhost:8080' &event.source.name !== '') return;
     // console.log(event.data.token,event.source);
        console.log(event.data.token)
      // Do we trust the sender of this message?  (might be
      // different from what we originally opened, for example).
      axios.post("http://localhost:8000/auth/convert-token", {
          grant_type: 'convert_token',
          token: event.data.token,
          backend: 'muni',
          client_id: 'TzSzxAFTIOgzD748aEdRHnXM97LjCH1Ny4t4bfCg',
          client_secret: 'R4MqFyMtZOCmbLGeSaxr58czfVBbIMZU4ROHHCBGO61hNyADZC8gx0fUBq8JWy8p6QTixStwSZ6D4TuRSA4sLjl2wnxD12rqN9LY31vxXh1wPU1ALLDlVVYnL0ve5B3l'
        }).then(response => {
          console.log(response)
      })

      //  alert('HURAAAAAAAAAAA')
      // event.source is popup
      // event.data is "hi there yourself!  the secret response is: rheeeeet!"
    },
  },
  created() {
    window.addEventListener("message", this.authCallback, false);
  },
  destroyed() {
      window.removeEventListener("message", this.authCallback);
  }
};
</script>
<style scoped>
#login {
  display: grid;
  place-items: center;
  height: 100%;
}
.munibtn {
  background-image: url("~@/assets/dark_cs-min.png");
  background-size: contain;
  width: 260px;
  height: 46px;
  cursor: pointer;
}
</style>