<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div>测试</div>
    <button @click="clickmi">测试接口</button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters(['name'])
  },
  methods: {
    clickmi() {
      this.$axios({
        method: 'get',
        url: 'http://120.77.183.17:8888/test/',
        data: ''
      }).then(res => {
        console.log(res.data.data)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
