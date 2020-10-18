<template>
  <div>
    <docsBlock

      v-bind:title="title"
      v-bind:endpoint_url="endpoint_url"
      v-bind:argsTable="argsTable"
      v-bind:isActive="isActive"

      v-bind:py_example="jobtitle_examples.get_py(endpoint_url)"
      v-bind:bash_example="jobtitle_examples.get_bash(endpoint_url)"
      v-bind:js_example="jobtitle_examples.get_js(endpoint_url)"
      v-bind:go_example="jobtitle_examples.get_go(endpoint_url)"

    ></docsBlock>
  </div>
</template>

<script>

import docsBlock from '@/components/docs/DocsBlock'
import { jobtitle_examples } from '@/components/docs/code_examples.js'

export default {

  name: 'docsOccupation',

  components: {
    docsBlock
  },

  data() {
    return {

      title: 'Endpoint: occupation',
      endpoint_url: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/job_title',
      argsTable: [
        ['input', 'string', 'first name last name'],
        ['filter_input (optional)', 'int', '1 to filter input by detecting name and surname, 0 not to. Default value 1'],
        ['use_proxy (optional)', 'int', '1 to use proxy while collecting data, 0 not to. Implemented due to bypass google/IG scrape detection. Default value 1'],
        ['ner_threshold (optional)', 'float', 'Detection probability threshold of word asociated with occupation/job-titles. Lower threshold implies looser detection. Default value 0.95 (returns words that are detected as occupation/job-title with probability of >95%)'],
        ['country_code (optional)', 'string', 'Country code through which to do the google search. Provide the value if known, this improves the results. <a href="https://developers.google.com/custom-search/docs/xml_results_appendices#countryCodes" target="_blank">Available country codes</a>. Default value us']
      ],
      isActive: 'Python',
      jobtitle_examples: jobtitle_examples,

    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
