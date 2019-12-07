<template>
  <div class="app-container">
    <!-- header -->
    <div>
      <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!-- <el-select v-model="listQuery.importance" placeholder="Imp" clearable style="width: 90px" class="filter-item">
        <el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select> -->
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <!-- <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加
      </el-button> -->
      <el-button class="filter-item" :disabled="selectdisble" style="margin-left: 10px;" type="danger" @click="handleModifyStatus()">
        批量删除
      </el-button>
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        下载
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox> -->
    </div>
    <!-- content -->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :default-sort="{prop: 'row.budget', order: 'ascending'}"
      @sort-change="sortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        align="center"
        type="selection"
        width="55"
        fixed="left"
      />
      <!-- <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <el-checkbox :ids="row.id" />
        </template>
      </el-table-column> -->
      <el-table-column label="计划名称" width="250px" fixed="left">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          <!-- <el-tag>{{ row.type | typeFilter }}</el-tag> -->
        </template>
      </el-table-column>
      <el-table-column label="状态" width="150px" align="center">
        <template slot-scope="{row}">
          <el-select :value="options[row.state]" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item"
              :label="item"
              :value="item"
            />
          </el-select>
        </template>
      </el-table-column>

      <el-table-column label="单元数" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.adGroupCount }}</span>
        </template>
      </el-table-column>
      <el-table-column label="关键词数" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.state }}</span>
        </template>
      </el-table-column>

      <el-table-column label="消耗上限" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.budget }}</span>
        </template>
      </el-table-column>

      <el-table-column label="消耗" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="展现次数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="点击次数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="平均点击花费" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="收藏店铺数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="收藏商品数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="询盘数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="点击率" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column v-if="showReviewer" label="点击率" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Imp" width="80px">
        <template slot-scope="{row}">
          <span>{{ row.keywordMode }}</span>
          <!-- <svg-icon v-for="n in + row.importance" :key="n" icon-class="star" class="meta-item__icon" /> -->
        </template>
      </el-table-column>
      <el-table-column label="Readings" align="center" width="95">
        <template slot-scope="{row}">
          <!-- <span v-if="row.pageviews" class="link-type" @click="handleFetchPv(row.pageviews)">{{ row.pageviews }}</span>
          <span v-else>0</span> -->
          <span>{{ row.budget }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Status" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.status">
            {{ row.budget }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 按钮功能 -->
      <el-table-column label="Actions" align="center" width="230" class-name="small-padding fixed-width" fixed="right">
        <template slot-scope="{row}">
          <el-button type="success" size="mini" @click="goodsPlan(row)">
            查看
          </el-button>
          <!-- <el-button type="primary" size="mini" @click="handleUpdate(row)">
            修改
          </el-button> -->
          <!-- <el-button v-if="row.status!='published'" size="mini" type="success" @click="handleModifyStatus(row,'published')">
            Publish
          </el-button>
          <el-button v-if="row.status!='draft'" size="mini" @click="handleModifyStatus(row,'draft')">
            Draft
          </el-button> -->
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleModifyStatus(row,'deleted')">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>

</template>

<script>
import { campaign, deletecampaign } from '@/api/getallplan' // api
import Pagination from '@/components/Pagination' // 分页组件
export default {
    components: { Pagination },
    data() {
        return {
            selectdisble: true,
            multipleSelection: {}, // 选择的值
            tableKey: 0, // 新增列表格
            options: {
                '1': '推广中',
                '-1': '手动暂停',
                '6': '不在投放时间下线，自动暂停'
            },
            total: 0, // 总页数
            listQuery: {// 双向数据绑定
                page: 1,
                limit: 10,
                importance: undefined,
                title: undefined,
                type: undefined,
                sort: '-id'
            },
            importanceOptions: [1, 2, 3], // 选择框
            calendarTypeOptions: [// 类型控制
                { key: 'CN', display_name: 'China' },
                { key: 'US', display_name: 'USA' },
                { key: 'JP', display_name: 'Japan' },
                { key: 'EU', display_name: 'Eurozone' }
            ],
            sortOptions: [// 排序选项
                { label: 'ID Ascending', key: '+id' },
                { label: 'ID Descending', key: '-id' }
            ],
            downloadLoading: false, // 下载exel
            showReviewer: false, // 新增列表格
            listLoading: true, // 内容loading
            list: [] // 总数据
        }
    },

    created() {
        this.getList()
    },
    methods: {
        // 获取数据
        getList() {
            // console.log('我是数据')
            campaign().then(res => {
                // console.log(res)
                const data = res.data.data.campaignVOList
                this.list = data.slice((this.listQuery.page - 1) * this.listQuery.limit, this.listQuery.page * this.listQuery.limit)
                this.total = data.length
                // console.log(data, data.length)
                this.listLoading = false
            }).catch(err => {
                console.log(err)
            })
        },
        // 搜索事件
        handleFilter() {
            this.listQuery.page = 1
            this.getList()
        },
        // add
        handleCreate() {
            console.log('我是添加')
            // this.$message({
            //     message: '我是添加',
            //     type: 'success'
            // })
        },
        // 下载exle文件
        handleDownload() {
            console.log('我是下载exle文件')
        },
        // 排序发生改变
        sortChange(data) {
            console.log(data, '我是排序功能')
        }, // 排序样式发生改变
        getSortClass: function(key) {
            console.log(key, '我是排序功能样式')
        },

        // 选中的值
        handleSelectionChange(val) {
            this.selectdisble = !(val.length > 0)
            const val1 = val
            let Selection = []
            for (let i = 0; i < val1.length; i++) {
                Selection.push(val1[i].id)
            }

            this.multipleSelection = Selection
        },
        // 修改标题
        handleUpdate(val) {
            console.log(val)
        },
        // 删除
        handleModifyStatus(val, status) {
            let campaignIds = ''
            const multipleSelection = this.multipleSelection

            let textInfo = ''
            if (status == 'deleted') {
                textInfo = '你确定要删除该计划吗？'
                campaignIds = val.id
            } else {
                textInfo = '您确认要删除所选的推广计划吗？'

                campaignIds = multipleSelection.join(',')
            }
            this.$confirm(textInfo, {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                deletecampaign({ campaignIds }).then(res => {
                    this.$message({
                        type: 'success',
                        message: '删除成功!'
                    })
                    this.getList()
                }).catch((err) => {
                    console.log(err)
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                })
            })
        },

        // 跳转推广单元商品
        goodsPlan(val) {
            const goodsId = val.id
            console.log(goodsId, '我是推广单元商品跳转')

            this.$router.push({ path: '/getallplan/addgoods', query: { id: goodsId }})
        }
    }
}
</script>

<style lang="scss" scoped>
.aa{
    font-family: 500
}
</style>
