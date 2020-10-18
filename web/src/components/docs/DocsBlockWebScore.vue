<template>
  <div>
    <docsBlock

      v-bind:title="title"
      v-bind:endpoint_url="endpoint_url"
      v-bind:argsTable="argsTable"
      v-bind:isActive="isActive"

      v-bind:py_example="webscore_examples.get_py(endpoint_url)"
      v-bind:bash_example="webscore_examples.get_bash(endpoint_url)"
      v-bind:js_example="webscore_examples.get_js(endpoint_url)"
      v-bind:go_example="webscore_examples.get_go(endpoint_url)"

    ></docsBlock>
  </div>
</template>

<script>

import docsBlock from '@/components/docs/DocsBlock'
import { webscore_examples } from '@/components/docs/code_examples.js'

export default {

  name: 'docsWebScore',

  components: {
    docsBlock
  },

  data() {
    return {

      title: 'Endpoint: web score',
      endpoint_url: 'https://namespy-api-mu7u3ykctq-lz.a.run.app/v1/web_score',
      argsTable: [
        ['input', 'string', 'first name last name'],
        ['filter_input (optional)', 'int', '1 to filter input by detecting name and surname, 0 not to. Default value 1'],
        ['use_proxy (optional)', 'int', '1 to use proxy while collecting data, 0 not to. Implemented to bypass google/IG scrape detection. Default value 1'],
        ['collected_data (optional)', 'int', 'return detailed data that is collected during the scoring process. Default value 1']
      ],
      isActive: 'Python',
      webscore_examples: webscore_examples,

    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
