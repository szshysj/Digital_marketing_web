<template>
  <div>
    <div>
      分词页面
      <!-- <input v-model="source" placeholder="化核加应子一箱24公斤湿乌梅子蜜饯果脯凉果散装批发潮汕特产">
      <button @click="get">提交</button> -->
      <div class="inline">
        <ul>
          <el-button
            v-for="(title, index) in value"
            :key="index"
            size="small"
            :index="index"
            :content="title"
            @click="get_title(title.t)"
          >{{ title.t }}</el-button>
        </ul>
      </div>
      <!-- <div>{{ words_title }}</div> -->
      <div>{{ keywords_gather }}</div>
      <div>{{ zzz }}</div>
      <!-- <div>{{ value }}</div> -->
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
        // 获取分词标签
        get_title(value) {
            console.log(value)
            this.words_title = value // 点击获取分词
            // this.category[0]// 类目信息
            this.$axios({
                method: 'get',
                url: 'http://120.77.183.17:8888/get/analyizer/result/',
                params: {
                    word: this.words_title,
                    category: this.category[0][0],
                    csrf_token: '1575283943246',
                    cookie2: '175203fa7876f0e9213abb3cfaa83e47'
                }}).then(res => {
                this.zzz = res
                console.log(res)
                alert('登陆成功')
            }).catch(() => {
                alert('登陆失败')
            })
        },
        // 进行分词
        get() {
            this.$axios({
                method: 'get',
                url: '/api/analyizer',
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
                console.log(res.data)
                this.value = res.data
                // this.cities = this.value.t
            })
        }
    }
}
</script>

<style lang="scss" scoped>
  .inline ul {
    list-style: none;
    /* border-bottom: 1px solid #7D7E80; */
  }
  .inline ul li {
    display: inline-block;
    width: 11%;
  }
</style>
