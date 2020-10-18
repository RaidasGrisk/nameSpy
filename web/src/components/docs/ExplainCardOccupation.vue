<template>
  <div class="card">
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4 has-text-centered has-text-success">Occupation</p>
        </div>
      </div>
      <div class="content">
        <p>
          <b>
            Occupation shows a list of occupation / job titles asociated with the provided name.
          </b>
        </p>

        <p>
          Here is the workflow: <br>
          1. Collect google search results (text you see when you google something) <br>
          2. Detect text language and translate it to English. <br>
          3. Run <a target="_blank" href="https://github.com/RaidasGrisk/jobtitle-detection">Machine Learning model</a>
          to detect words or phrases related to occupation / job titles.
        </p>

        <p>
          To give you an idea here is an example of model output for google search results for Albert Einstein:
        </p>

         <div class="table-container">
          <table class="table">
            <tbody>
              <tr><th></th></tr>
              <tr>
                <th>Albert Einstein - Wikipedia</th>
              </tr>
              <tr>
                <td>
                  Albert Einstein was a German-born
                  <a class="has-text-success has-text-weight-bold" title="Confidence: 0.897">theoretical physicist</a>
                  who developed the theory of relativity, one of the two pillars
                  of modern physics (alongside quantum ... <br> <br>
                </td>
              </tr>
              <tr>
                <th>Albert Einstein | New Scientist</th>
              </tr>
              <tr>
                <td>
                  Albert Einstein is arguably the most influential
                  <a class="has-text-success has-text-weight-bold" title="Confidence: 0.951">scientist</a>
                  of the 20th century. His general theory of relativity changed our
                  understanding of space and time, ...
                </td>
              </tr>
            </tbody>
          </table>
         </div>

      </div>
    </div>
  </div>

</template>

<script>


export default {

  name: 'ExplainCardOccupation',

  components: {
  },

  props: {
  },

  data() {
    return {
    }
  }

}
</script>


<style scoped>

</style>
