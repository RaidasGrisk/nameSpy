<template>
  <section class="section">
    <div id="google-signin-btn"></div>
    <a href="#" class="sign-out" @click="signOut" v-if="profile">Sign out</a>

    <div v-if="profile">
      <pre>{{ profile }}</pre>
    </div>

  </section>
</template>

<script>

// https://developers.google.com/identity/sign-in/web/sign-in
// https://stackoverflow.com/a/58809376

export default {
  name: 'Login',

  data() {
    return {
      profile: false
    }
  },

  methods: {

    renderGoogleLoginButton() {
      window.gapi.signin2.render("google-signin-btn", {
        onsuccess: this.onSignIn
      });
    },

    onSignIn(googleUser) {
      var profile = googleUser.getBasicProfile();
      this.profile = profile;

      // The ID token you need to pass to your backend:
      var id_token = googleUser.getAuthResponse().id_token;
      this.profile.id_token = id_token
    },

    signOut() {
      var vm = this
      var auth2 = window.gapi.auth2.getAuthInstance();
      auth2.signOut().then(function () {
        vm.profile = false
      });
    }

  },

  mounted() {
    window.addEventListener("google-loaded", this.renderGoogleLoginButton);
  }

}
</script>

<style scoped>

</style>
