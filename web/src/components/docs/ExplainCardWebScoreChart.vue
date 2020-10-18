<template>
  <div class="frameworks">
  <section class='framework'>
    <header class='framework__header'>
    </header>
    <div class='framework__data'>
      <div class='framework__data-info'>
        <div class='framework__period'>
          <span class='framework__period-text has-text-success'>{{info.label}}</span>
        </div>
        <strong class='framework__downloads'>{{info.value}}</strong>
      </div>
      <trend-chart :datasets='[data]' :min='0' padding='5 5 0' :interactive='true' @mouse-move='onMouseMove'></trend-chart>
    </div>
  </section>
  </div>
</template>

<script>

import Vue from 'vue';
import TrendChart from 'vue-trend-chart';
Vue.use(TrendChart);

export default {

  name: 'ExplainCardWebScoreCard',

  data() {
    return {
      name: 'Web score',
      currentInfo: null,
      data:
        {
          data: [
            {'value': -1.00, 'name': 'totally unknown person'},
            {'value': -1.00, 'name': 'totally unknown person'},
            {'value': -1.00, 'name': 'totally unknown person'},
            {'value': -1.00, 'name': 'totally unknown person'},
            {'value': -0.99, 'name': 'totally unknown person'},
            {'value': -0.99, 'name': 'totally unknown person'},
            {'value': -0.98, 'name': 'totally unknown person'},
            {'value': -0.97, 'name': '-'},
            {'value': -0.96, 'name': '-'},
            {'value': -0.94, 'name': '-'},
            {'value': -0.90, 'name': '-'},
            {'value': -0.84, 'name': '-'},
            {'value': -0.76, 'name': '-'},
            {'value': -0.63, 'name': 'Conah Paine'},
            {'value': -0.46, 'name': 'Fariha Bonilla'},
            {'value': -0.24, 'name': '-'},
            {'value': 0.00, 'name': 'average person'},
            {'value': 0.12, 'name': 'Melina Weber'},
            {'value': 0.24, 'name': 'Paulius Gritėnas'},
            {'value': 0.46, 'name': 'Sophie Goldsmith'},
            {'value': 0.63, 'name': '-'},
            {'value': 0.76, 'name': 'Charles Darwin'},
            {'value': 0.80, 'name': 'Charles Darwin'},
            {'value': 0.84, 'name': 'Karolina Meschino'},
            {'value': 0.88, 'name': 'Karolina Meschino'},
            {'value': 0.90, 'name': '-'},
            {'value': 0.94, 'name': '-'},
            {'value': 0.96, 'name': '-'},
            {'value': 0.97, 'name': 'Bart Simpson'},
            {'value': 0.97, 'name': 'Bart Simpson'},
            {'value': 0.98, 'name': '-'},
            {'value': 0.99, 'name': 'Albert Einstein'},
            {'value': 0.99, 'name': 'Albert Einstein'},
            {'value': 1.00, 'name': 'Nicki Minaj'},
            {'value': 1.00, 'name': 'Nicki Minaj'},
            {'value': 1.00, 'name': 'Nicki Minaj'}
          ],
          fill: true,
          smooth: true,
        },
    }
  },

  computed: {

    info() {
      return {
        label: this.currentInfo ? this.currentInfo.label : 'average person',
        value: this.currentInfo ? this.currentInfo.value : '0.00'
      }
    }
  },

  methods: {
    onMouseMove(params) {
      if (!params) {
        this.currentInfo = null;
        return;
      }
      this.currentInfo = {
        label: params.data[0].name,
        value: params.data[0].value
      };
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang='scss'>

.frameworks {
  display: flex;
  // flex-wrap: wrap;
  // align-items: center;  // added
  // justify-content: space-between;  // added
  .vtc {
    width: 160px;
    height: 60px;
    // margin-right: -5px;
    margin-bottom: -5px;
  }
  .stroke {
    stroke-width: 3;
  }
  .fill {
    opacity: 0.2;
  }
  .active-line {
    stroke: rgba(0, 0, 0, 0.2);
  }
  // .point {
  //   display: none;
  // }
  // .point.is-active {
  //   display: block;
  // }
}
.framework {
  width: 110%;
  border-bottom: 1px solid rgba(#7510F7, 0.8);

  &__period {
    // display: flex;
    // align-items: left;
    // flex-shrink: 0;
    &-text {
      font-size: 16px;
      line-height: 36px;
      // white-space: nowrap;
    }
  }
  &__data {
    // display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
  &__downloads {
    // opacity: 0.5;
    color: #7510F7;
    // display: flex; // added
    font-size: 16px;
  }
}
.curve {
  .stroke {
    stroke: #7510F7;
  }
  .fill {
    fill: #7510F7;
  }
  // currentInfo
  // .point {
  //   fill: #7510F7;
  //   stroke: #7510F7;
  // }
}

</style>
