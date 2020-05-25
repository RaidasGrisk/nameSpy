<template>
  <footer class="footer is-primary">
    <!-- style="border-top: 2px solid #F0F0F0;" -->
    <div class="container">
      <div class="content has-text-centered has-text-white-ter is-size-7">
        <div class="section">
          <div class="content has-text-success">
            <b>NameSpy</b><br>
          </div>
          <div class="content">
            Care for more info?<br>
            Drop a message
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
  background-color: #673AB7;
}
</style>
