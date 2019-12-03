<template>
  <div>
    <div>
      分词页面
      <input v-model="source" placeholder="化核加应子一箱24公斤湿乌梅子蜜饯果脯凉果散装批发潮汕特产">
      <button @click="get">提交</button>
      <div>{{ value }}</div>
    </div>
    <!-- 分词数据渲染 -->
    <div class="dataEach">
      <el-row :gutter="20">
        <!-- 左边 -->
        <el-col :span="12">
          <div class="btnTop" style="visibility: hidden;">
            <el-row>
              <el-col :span="12">
                <p>已添加12个关键词</p>
              </el-col>
              <el-col :span="12">
                <el-button type="warning">批量删除</el-button>
              </el-col>
            </el-row>
          </div>
          <el-table
            ref="multipleTable"
            v-loading="listLoading"
            :data="tableData"
            style="width: 100%"
            :default-sort="{prop: 'date', order: 'descending'}"
            :header-cell-style="{background:'#F5F7FA'}"
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
            <el-row>
              <el-col :span="12">
                <p>已添加{{ this.keyword.length }}个关键词</p>
              </el-col>
              <el-col :span="12">
                <el-button type="warning" @click="handleModifyStatus()">批量删除</el-button>
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

            <el-table-column align="center" label="PC端出价" width="280" prop="pc">
              <template slot-scope="{row}">
                <keywordShow :row="row" :offpc="pc" />
              </template>
            </el-table-column>

            <el-table-column align="center" label="移动端出价" width="280" prop="pv">
              <template slot-scope="{row}">
                <keywordShow :row="row" :offpc="pv" />
              </template>
            </el-table-column>

            <!-- 按钮功能 -->
            <el-table-column label="操作" align="center" width="150" class-name="small-padding fixed-width" type="index">
              <template slot-scope="{row,$index}">
                <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleModifyStatus(row,$index)">
                  删除{{ $index }}
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
  </div>
</template>

<script>
import { analyizerResult } from '@/api/keyword' // api
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
            listLoading: true, // 加载动画
            source: '化核加应子一箱24公斤湿乌梅子蜜饯果脯凉果散装批发潮汕特产',
            value: [], // { "t": "化核", "p": "0.945319" }, { "t": "加应子", "p": "0.87609" },
            keyword: [], // 选择关键词
            tableData: [], // 分好词数据
            selsectAll: null, // 选中的row
            pc: 'pc',
            pv: 'pv'
        }
    },
    created() {
        // let title = this.$route.query.title
        // console.log(title)
        // alert(title)
        // 获取所有分词关键词

    },
    methods: {
        get() {
            this.$axios({
                method: 'get',
                url: '/analyizer/get.php',
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
        },
        // 分词按钮
        butanalyizer() {
            let json = {}
            json['word'] = '凉果'
            json['category'] = '李子干'
            analyizerResult(json).then(res => {
                console.log(res)
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
            console.log(row)
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
        }

    }
}
</script>

<style lang="scss" scoped>

</style>
