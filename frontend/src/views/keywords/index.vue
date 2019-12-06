<template>
  <div v-loading="titleLoading" class="app-container">
    <div class="inline">
      <ul>
        <el-button
          v-for="(title, index) in part_titile"
          :key="index"
          size="small"
          :index="index"
          :content="title"
          :class="{ 'btnshow': title === btnshow }"
          @click="butanalyizer(title)"
        >{{ title }}</el-button>
      </ul>
    </div>
    <!-- 分词数据渲染 -->
    <div class="dataEach">
      <el-row :gutter="20">
        <!-- 左边 -->
        <el-col :span="12">

          <div class="btnTop">
            <el-row>
              <el-col :span="12">
                <p>点击率为排序</p>
              </el-col>

            </el-row>
          </div>
          <el-table
            ref="multipleTable"
            v-loading="listLoading"
            :data="tableData"
            style="width: 100%"
            :default-sort="{prop: '_source.leftavgclick7days', order: 'descending'}"
            :header-cell-style="{background:'#F5F7FA'}"
            height="600"
            @selection-change="clickRow"
          >
            <el-table-column
              align="center"
              type="selection"
              width="55"
            />
            <el-table-column
              prop="_source.keyword"
              align="center"
              label="关键词"
              width="120"
            />

            <el-table-column align="center" label="推荐理由" width="120">
              <template slot-scope="{row}">
                {{ row._source.recommendtags | arrTOstring }}
              </template>
            </el-table-column>

            <el-table-column
              align="center"
              prop="_source.searchavg7days"
              label="展示指数"
              sortable
              width="120"
            />

            <el-table-column align="center" label="平均出价" width="120" prop="_source.leftavgpv7days" sortable>
              <template slot-scope="{row}">
                {{ row._source.leftavgpv7days | rounding(2) }}
              </template>
            </el-table-column>

            <el-table-column
              align="center"
              prop="_source.countbuyer"
              label="竞争指数"
              sortable
              width="120"
            />
            <el-table-column align="center" label="点击率" width="120" prop="_source.leftavgclick7days" sortable>
              <template slot-scope="{row}">
                {{ row._source.leftavgclick7days | rounding(2) }}%
              </template>
            </el-table-column>

            <!-- 暂无数据 -->
            <template slot="empty">
              <p>暂无数据</p>
            </template>
          </el-table>
        </el-col>
        <!-- 右边 -->
        <el-col :span="12">
          <div class="btnTop">
            <el-row :gutter="24">
              <el-col :span="18">
                <p>已添加{{ this.keyword.length }}个关键词</p>
              </el-col>
              <el-col :span="2" :offset="2">
                <el-button type="warning" class="btuncolor" @click="handleModifyStatus()">批量删除</el-button>
              </el-col>
            </el-row>
          </div>
          <el-table
            :data="keyword"
            style="width: 100%"
            :header-cell-style="{background:'#F5F7FA'}"
            @selection-change="clickRow"
          >

            <el-table-column
              prop="keyword"
              align="center"
              label="关键词"
              width="120"
            />

            <el-table-column align="center" label="PC端出价" min-width="250" prop="pc">
              <template slot-scope="{row}">
                <keywordShow :row="row" :offpc="pc" />
              </template>
            </el-table-column>

            <el-table-column align="center" label="移动端出价" min-width="250" prop="pv">
              <template slot-scope="{row}">
                <keywordShow :row="row" :offpc="pv" />
              </template>
            </el-table-column>

            <!-- 按钮功能 -->
            <el-table-column label="操作" align="center" width="150" class-name="small-padding fixed-width" type="index">
              <template slot-scope="{row,$index}">
                <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleModifyStatus(row,$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>

            <!-- 暂无数据 -->
            <template slot="empty">
              <p>暂无数据</p>
            </template>

          </el-table>
        </el-col>

      </el-row>
    </div>
    <!-- 提交 -->
    <div class="buttsuee">

      <span class="btuncolor btnpadd" @click="clickKeyword">保存并继续</span>

    </div>
  </div>
</template>

<script>
import { analyizerResult, offerkeyword, getAllKeyword, getCpckeyword, getAdgropInfo, updata } from '@/api/keyword' // api
import keywordShow from '@/components/Getallplan/keywordShow.vue' // 分页组件
export default {
    // 组件
    components: { keywordShow },
    // 过滤器
    filters: {
        // 正则转
        arrTOstring(value) {
            let data = value.replace(/\s*'|'|\[|]|,/g, ' ')
            return data
        },
        // 四舍五入
        rounding(value, num) {
            let vas = parseFloat(value)
            return vas.toFixed(num)
        }
    },
    data() {
        return {
            listLoading: false, // 加载动画
            titleLoading: true,
            keyword: [], // 选择关键词
            tableData: [], // 分好词数据
            selsectAll: null, // 选中的row
            pc: 'pc',
            pv: 'pv',
            campaignId: null, // 推广计划id
            adGroupIdList: null, // 推广单元id
            btnshow: '', // 按钮样式
            // 太有
            key_all: [], // 所有关键词
            key_cpc: [], // cpc单个关键词
            key_all_index: [], // recommendTags，keyword
            key_cpc_all: [], // cpc 所有关键词
            keywords_gather: [], // 整合后的数据
            month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], // 进行月份枚举
            category: [], // 类目信息
            source: '获取标题信息',
            words_title: '', // 存放点击时的标签值
            value: [], // { "t": "化核", "p": "0.945319" }, { "t": "加应子", "p": "0.87609" },
            part_titile: [] // 去重后分词标题['奶糖'，'糖果']
        }
    },
    created() {
        // 获取id
        const campaignId = this.$route.query.campaignId
        const adGroupIdList = this.$route.query.adGroupIdList
        this.campaignId = campaignId
        this.adGroupIdList = adGroupIdList
        let allwords = {}
        allwords['campaignId'] = this.campaignId
        allwords['adGroupIdList'] = this.adGroupIdList

        // 获取所有关键词 & 获取所有cpc关键词
        getAllKeyword(allwords).then(res => {
            // 遍历数组，并获取keywod,recommendTags值
            for (let v of Object.values(res.data.data.recommendKeywordVOList)) {
                this.key_all.push(v.keyword)
                this.key_all_index.push({ keyword: v['keyword'], recommendTags: v['recommendTags'] })
            }
            this.key_all = this.key_all.join(',')
            // 获取cpc 所有关键词
            let cpckeywords = {}
            cpckeywords['keywords'] = this.key_all
            getCpckeyword(cpckeywords).then(res => {
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
                this.upload_data()
            }).catch(() => {
                alert('获取cpc失败')
            })
        }).catch(() => {
            alert('获取所有关键词失败')
        })
        // 获取类目信息
        let info = {}
        info['adGroupIds'] = this.adGroupIdList
        getAdgropInfo(info).then(res => {
            this.category = res.data.data.adGroupVOList
            this.category = this.category.map(item => {
                return [item.category, item.title]
            })
            // 进行分词
            this.get()
        }).catch(() => {
            alert('整合类目&标题信息失败')
        })
    },
    methods: {

        // 进行分词
        get() {
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
                // 将获取的分词通过p 参数的大小进行反向排序
                res.data.sort(function(a, b) {
                    a.p = parseFloat(a.p)
                    b.p = parseFloat(b.p)
                    return b.p - a.p
                })
                this.value = res.data
                // 分词去重
                this.part_titile = this.value.map(list => {
                    return list.t
                })
                this.part_titile = [...new Set(this.part_titile)]
                this.titleLoading = false
            })
            // this.key_words()
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
            let datas = {}
            datas['keyword_list'] = this.keywords_gather
            updata(datas).then(res => {
                console.log('上传成功')
            }).catch(() => {
                console.log('上传失败')
            })
        },
        // 分割线----------------------------------------------------------------------
        // 分词按钮
        butanalyizer(value) {
            this.btnshow = value
            this.listLoading = true
            let json = {}
            json['word'] = value
            json['category'] = this.category[0][0]
            analyizerResult(json).then(res => {
                const hist = res.data.hits.hits
                this.tableData = hist
                this.listLoading = false
            }).catch(err => {
                console.log(err)
            })
        },
        // 格式化所有列
        formatter(row, column) {
            return row.address
        },
        // 点击多选框
        clickRow(row) {
            let rowData = row
            let arrKey = []
            for (let i = 0; i < rowData.length; i++) {
                let json = {}
                json['keyword'] = rowData[i]._source.keyword
                json['pc'] = rowData[i]._source.leftavgpv7days
                json['pv'] = rowData[i]._source.leftavgpv7days
                arrKey.push(json)
            }
            // 赋值选中的值
            this.selsectAll = row
            // 整理好的数据
            this.keyword = arrKey
        },
        // 删除
        handleModifyStatus(row, index) {
            console.log(index)
            if (row) {
                this.$refs.multipleTable.toggleRowSelection(this.selsectAll[index])
            } else {
                this.$refs.multipleTable.clearSelection()
            }
        },
        // 子方法修改pc
        updataPc(row, data) {
            console.log('rows', row, data)
        },
        // 提交关键词
        clickKeyword() {
            let keywords = []
            let bidPrices = []
            let keydata = this.keyword
            let json = {}
            for (let i = 0; i < keydata.length; i++) {
                keywords.push(keydata[i].keyword)
                bidPrices.push(parseFloat(keydata[i].pc).toFixed(1) + '_' + parseFloat(keydata[i].pv).toFixed(1))
            }
            keywords = keywords.join('@@@')
            bidPrices = bidPrices.join(',')
            json['campaignId'] = this.campaignId
            json['adGroupIdList'] = this.adGroupIdList
            json['keywords'] = keywords
            json['bidPrices'] = bidPrices
            offerkeyword(json).then(res => {
                const textErr = res.data.data.ErrorKeywordList
                let errText = []
                if (textErr.length != 0) {
                    for (var i = 0; i < textErr.length; i++) {
                        errText.push(textErr[i].keyword + '=>' + textErr[i].keywordAddErrorReason)
                    }
                    errText = errText.join('<br>')
                    this.$message.error({
                        dangerouslyUseHTMLString: true,
                        message: `<strong>${errText}</strong>`
                    })
                } else {
                    this.$message.success({
                        message: '成功'
                    })
                }

                // 跳转到推广计划下所有推广单元
                this.$router.push({ path: '/getallplan/addgoods', query: { id: this.campaignId }})
            }).catch(err => {
                console.log(err)
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
  .buttsuee{
      margin-top: 20px;
      text-align: right;
      background: #F4F4F8;
     border: 1px solid hsla(0,0%,50%,.2);
  }
  // 点按钮样式
  .btnshow{
      background: #ecf5ff;
  }
  .btuncolor{
      background: #ff6000
  }
  //提交关键字按钮
  .btnpadd{
      width: 130px;
    height: 58px;
    display: inline-block;
    color: #fff;
    text-align: center;
    line-height: 58px;
  }
</style>
