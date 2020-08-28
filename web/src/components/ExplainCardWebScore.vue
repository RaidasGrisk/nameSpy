<template>
  <div class="card">
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4 has-text-centered has-text-success">Web Score</p>
        </div>
      </div>
      <div class="content">
        <p><b>
          Web score shows how well a given name is known on the internet.
        </b></p>

        <p>
          First it collects the publicly available data on social networks and google (numbers of followers, google search results etc).
          Then, based on average population metrics, it analizes and combines the data to make a web score of a given name.
          The score ranges between -1 and 1, where 0 is an average person, 1 is a super-mega star and -1 is totally unknown.
        </p>

        <p>
          To give you an idea here are some examples:
        </p> <br>

        <div class="columns is-four-fifths is-centered">
          <ExplainCardWebScoreChart />
        </div>

      </div>
    </div>
  </div>
</template>

<script>

import ExplainCardWebScoreChart from './ExplainCardWebScoreChart'

export default {

  name: 'ExplainCardWebScore',

  components: {
    ExplainCardWebScoreChart
  },

  data() {
    return {
    }
  }

}
</script>


<style scoped>

</style>
