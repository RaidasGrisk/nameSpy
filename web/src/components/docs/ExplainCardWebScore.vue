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
          Here is the workflow: <br>
          1. Collect publicly available data on social networks / google / wikipedia. <br>
          2. Analize and combine the data to make a web score besed on average population metrics. <br>
          <br>
          The score ranges between -1 and 1, where 0 is an average name, 1 is a super star and -1 is totally unknown.
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

import ExplainCardWebScoreChart from '@/components/docs/ExplainCardWebScoreChart'

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
