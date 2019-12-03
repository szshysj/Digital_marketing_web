<template>
  <div>
    <div>
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
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            key_all: [], // 所有关键词
            key_cpc: [], // cpc单个关键词
            key_all_index: [], // recommendTags，keyword
            key_cpc_all: [], // cpc 所有关键词
            keywords_gather: [], // 整合后的数据
            month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], // 进行月份枚举
            category: [], // 类目信息
            source: '获取标题信息',
            words_title: '', // 存放点击时的标签值
            value: [] // { "t": "化核", "p": "0.945319" }, { "t": "加应子", "p": "0.87609" },
        }
    },
    created() {
        this.value_t = this.value.t
        // 获取所有关键词 & 获取所有cpc关键词
        this.$axios({
            method: 'get',
            url: 'http://120.77.183.17:8888/get/offer/keyword/',
            params: {
                'csrf_token': '1575283943246',
                'cookie2': '175203fa7876f0e9213abb3cfaa83e47',
                'campaignId': '817274318',
                'adGroupIdList': '394115593'
            }
        }).then(res => {
            // 遍历数组，并获取keywod,recommendTags值
            for (let v of Object.values(res.data.data.recommendKeywordVOList)) {
                this.key_all.push(v.keyword)
                this.key_all_index.push({ keyword: v['keyword'], recommendTags: v['recommendTags'] })
            }
            this.key_all = this.key_all.join(',')
            // 获取cpc 所有关键词
            this.$axios({
                method: 'post',
                url: 'http://120.77.183.17:8888/post/offer/keyword/cpc/',
                data: {
                    csrf_token: '1575283943246',
                    cookie2: '175203fa7876f0e9213abb3cfaa83e47',
                    keywords: this.key_all
                }
            }).then(res => {
                for (let cpc_selected of Object.values(res.data.data.listVOREST)) {
                    this.key_cpc = cpc_selected
                    // 提取关键的键值放入key_cpc_all 数组
                    this.key_cpc_all.push({
                        gmtCreate: cpc_selected['gmtCreate'],
                        keyword: cpc_selected['keyword'],
                        countBuyer: cpc_selected['countBuyer'],
                        leftAvgClick7days: cpc_selected['leftAvgClick7days'],
                        leftAvgPV7days: cpc_selected['leftAvgPV7days'],
                        searchAvg7days: cpc_selected['searchAvg7days']
                    })
                }
                this.key_words()
            }).catch(err => {
                console.log(err.response)
                alert('获取cpc失败')
            })
        }).catch(err => {
            console.log(err.response)
            alert('获取所有关键词失败')
        })
        // 获取类目信息
        this.$axios({
            method: 'get',
            url: 'http://120.77.183.17:8888/get/campaign/adgroup/info/',
            params: {
                csrf_token: '1575283943246',
                cookie2: '175203fa7876f0e9213abb3cfaa83e47',
                'adGroupIds': '394115593' // 推广单元id
            }
        }).then(res => {
            this.category = res.data.data.adGroupVOList
            this.category = this.category.map(item => {
                return [item.category, item.title]
            })
            // 进行分词
            this.get()
        }).catch(err => {
            console.log(err.response)
            alert('整合类目&标题信息失败')
        })
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
                console.log(res)
            }).catch(() => {
                alert('登陆失败')
            })
        },
        // 进行分词
        get() {
            console.log(this.category[0][1])
            let sources = this.category[0][1]
            this.$axios({
                method: 'get',
                url: '/analyizer/get.php',
                params: {
                    source: sources,
                    param1: 0,
                    param2: 1,
                    json: 1
                }}).then(res => {
                console.log(res)
                // 将获取的分词通过p 参数的大小进行反向排序
                res.data.sort(function(a, b) {
                    a.p = parseFloat(a.p)
                    b.p = parseFloat(b.p)
                    return b.p - a.p
                })
                this.value = res.data
            })
            this.key_words()
        },
        // 合并关键词
        key_words() {
            for (let x of this.key_all_index) {
                for (let y of this.key_cpc_all) {
                    if (x.keyword === y.keyword) {
                        var zero = y.gmtCreate.split(' ')[3] // 提取 10：15：32
                        var day = y.gmtCreate.split(' ')[2] // 提取 27
                        var datas = y.gmtCreate.replace(zero, '') // 将 10：15：32删除,使.getData()获取日期正常
                        var born = new Date(datas)
                        y.gmtCreate = born.getFullYear() + '-' + this.month[born.getMonth()] + '-' + day + ' ' + zero // 获取日期2019-11-27 10：15：32
                        // 获取的值存在一个一维数组内
                        this.keywords_gather.push([
                            x.keyword,
                            x.recommendTags,
                            y.countBuyer,
                            parseFloat(y.leftAvgClick7days.toFixed(2)),
                            parseFloat(y.leftAvgPV7days.toFixed(2)),
                            y.searchAvg7days,
                            this.category[0][0], // 类目信息
                            y.gmtCreate
                        ]
                        )
                        break
                    }
                }
            }
        },
        // 上传关键词
        upload_data() {
            this.$axios({
                method: 'post',
                url: 'http://120.77.183.17:8888/post/mysql/keyword/',
                data: {
                    keyword_list: this.keywords_gather
                }
            }).then(res => {
                console.log(res)
                console.log('上传成功')
            })
            console.log(this.keywords_gather)
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
