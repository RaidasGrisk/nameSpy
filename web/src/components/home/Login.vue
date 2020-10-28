<template>
  <section class="section">
    <div class="card">
      <header class="card-header">
        <p class="card-header-title is-centered">
          Sign In or Up
        </p>
      </header>
      <div class="card-content">
        <div class="content">
          <!-- google -->
          <div id="google-signin-btn"></div>
          <!-- Github -->
          <!-- <a @click="GithubSignin" class="btn btn-social btn-github">
            <i class="fa fa-github"></i>Github
          </a> -->

        </div>
        <div v-if="profile">
          <pre>{{ profile }}</pre>
        </div>
      </div>
      <footer class="card-footer">
        <!-- v-if="profile" -->
        <a href="#" class="card-footer-item" @click="signOut">Logout</a>
      </footer>
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

    // Google
    renderGoogleLoginButton() {
      window.gapi.signin2.render("google-signin-btn", {
        onsuccess: this.onSignIn
      });
    },

    onSignIn(googleUser) {
      var profile = googleUser.getBasicProfile();

      // The ID token you need to pass to your backend:
      var id_token = googleUser.getAuthResponse().id_token;
      profile.id_token = id_token

      this.profile = profile;

    },

    // GitHub
    // https://jsfiddle.net/dg9h7dse/30/
    // https://coderwall.com/p/-b6-ag/implement-social-login-button-for-any-oauth-provider-using-vue-js
    // GithubSignin() {
    //   // Initialize with your OAuth.io app public key
    //   window.OAuth.initialize('99f7d97c101527b9b89c');
    //   // Use popup for oauth
    //   // Alternative is redirect
    //   window.OAuth.popup('github').then(github => {
    //     console.log('github:', github);
    //     // Retrieves user data from oauth provider
    //     // Prompts 'welcome' message with User's email on successful login
    //     // #me() is a convenient method to retrieve user data without requiring you
    //     // to know which OAuth provider url to call
    //     github.me().then(data => {
    //       console.log('me data:', data);
    //       alert('GitHub says your email is:' + data.email + ".\nView browser 'Console Log' for more details");
    //     });
    //     // Retrieves user data from OAuth provider by using #get() and
    //     // OAuth provider url
    //     github.get('/user').then(data => {
    //       console.log('self data:', data);
    //     })
    //   });
    // },

    // Common
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
