<template>
  <footer class="footer has-background-primary">
    <!-- style="border-top: 2px solid #F0F0F0;" -->
    <div class="container">
      <div class="content has-text-centered has-text-white-ter is-size-7">
        <div class="section">
          <div class="content has-text-success">
            <b>NameSpy</b><br>
          </div>
          <div class="content">
          </div>

          <div class="buttons is-centered">

              <a href="https://twitter.com/raidasg" class="button is-success is-link" target="_blank">
                <span class="icon">
                  <font-awesome-icon :icon="['fab', 'twitter']" />
                </span>
              </a>

              <a href="https://github.com/RaidasGrisk/" class="button is-success is-link" target="_blank">
                <span class="icon">
                  <font-awesome-icon :icon="['fab', 'github']" />
                </span>
              </a>

          </div>

          <div class="content has-text-grey-darker">
            Made with<br>
            <img src="@/assets/vue.png" alt="Logo" style="width:20px;">
            <img src="@/assets/python.png" alt="Logo" style="width:24px;">
            <img src="@/assets/mongodb.png" alt="Logo" style="width:24px;">
            <img src="@/assets/gcp.png" alt="Logo" style="width:24px;">
          </div>

        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {

    }
  }
}
</script>

<style scoped>

.footer {
  padding-bottom: 2rem;
}
</style>
