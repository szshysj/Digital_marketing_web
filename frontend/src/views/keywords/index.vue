<template>
  <div>
    <div>
      分词页面
      <input v-model='source' placeholder="化核加应子一箱24公斤湿乌梅子蜜饯果脯凉果散装批发潮汕特产"/>
      <button @click="get">提交</button>
      <div>{{ value }}</div>
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            source: '化核加应子一箱24公斤湿乌梅子蜜饯果脯凉果散装批发潮汕特产',
            value: [] // { "t": "化核", "p": "0.945319" }, { "t": "加应子", "p": "0.87609" },
        }
    },
    created() {
        // let title = this.$route.query.title
        // console.log(title)
        // alert(title)
    },
    methods: {
        get() {
             this.$axios({
                method: 'get',
                url: 'http://120.77.183.17/analyizer',
                params: {
                    source: this.source,
                    param1: 0,
                    param2: 1,
                    json: 1
                }}).then(res => {
                console.log(res)
                alert('登陆成功')
                // 将获取的分词通过p 参数的大小进行反向排序
                res.data.sort(function(a, b) {
                    a.p = parseFloat(a.p)
                    b.p = parseFloat(b.p)
                    return b.p - a.p
                })
                this.value = res
            })
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
