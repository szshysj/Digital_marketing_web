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
                method: 'post',
                url: 'http://120.77.183.17/post/user/info/',
                data: { 'csrf_token': '1573795599377', 'cookie2': '10e017de5b8669225b455d6afe59485c' }
            }).then(res => {
                console.log(res)
            }).catch(err => {
                console.log(err.response.data.cookie2)
                alert(err.response.data.cookie2)
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
