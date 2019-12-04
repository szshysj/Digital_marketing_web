<template>
  <div class="app-container">
    <!-- header -->
    <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="addcell">
        加入计划
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="get_cell()">
        测试按钮
      </el-button>
    </div>
    <!-- content -->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list.slice((listQuery.page-1)*listQuery.limit,listQuery.page*listQuery.limit)"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :default-sort="{prop: 'id', order: 'ascending'}"
      @sort-change="sortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column
        align="center"
        type="selection"
        width="55"
        fixed="left"
      />
      <el-table-column label="单元名称" width="250px" fixed="left">
        <template slot-scope="{row}">
          <span class="link-type">{{ row.title }}</span>
          <!-- <el-tag>{{ row.type | typeFilter }}</el-tag> -->
        </template>
      </el-table-column>

      <el-table-column label="图片" width="150px" align="center">
        <template slot-scope="{row}">
          <img :src="row.imgUrl" alt="">
        </template>
      </el-table-column>

      <el-table-column label="推广状态" width="150px" align="center">
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

      <el-table-column label="商品状态" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.state }}</span>
        </template>
      </el-table-column>

      <el-table-column label="类目" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.budget }}</span>
        </template>
      </el-table-column>

      <el-table-column label="关键词数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
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

      <el-table-column v-if="showReviewer" label="点击率" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.priceMode }}</span>
        </template>
      </el-table-column>

    </el-table>

    <!-- 分页 -->
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

  </div>
</template>

<script>
import { campaignAdgroup, campaignAdgroupInfo } from '@/api/getallplan' // api
import Pagination from '@/components/Pagination' // 分页组件
export default {
    components: { Pagination },
    data() {
        return {

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
            list: [], // 总数据
            campaignId: '' // 推广计划id
        }
    },
    created() {
        // this.getList()
        this.get_cell()
    },
    methods: {
        // 获取已经创建的推广单元
        get_cell() {
            let id = this.$route.query.id
            let params = {}
            params['campaignId'] = id
            this.campaignId = id
            console.log('获取推广单元1')
            this.$axios({
                method: 'get',
                url: 'http://120.77.183.17:8888/get/offer/',
                params: {
                    'csrf_token': '1575283943246',
                    'cookie2': '175203fa7876f0e9213abb3cfaa83e47',
                    'campaignId': this.campaignId,
                    'skip': '1' // 页数
                }
            }).then((res) => {
                console.log(res.data.data.promoteOfferList)
                console.log('获取推广单元')
                const dataok = res.data.data.promoteOfferList
                this.list = dataok
                this.total = dataok.length
                this.listLoading = false
            }).catch(err => {
                console.log(err.response)
                alert('获取cpc失败')
            })
        },
        // 搜索事件
        handleFilter() {
            this.listQuery.page = 1
            this.getList()
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
            this.multipleSelection = val
            console.log(val)
        },
        // 将单元加入推广计划
        addcell() {
            console.log('添加单元')
            // let id = this.$route.query.id
            // let params = {}
            // params['campaignId'] = id
            // const title = val.title
            // // 将推广计划IP传入添加单元页面
            // this.$router.push({ path: '/getallplan/addcell', query: { id: params.campaignId, title: title }})
        }
    }
}
</script>

<style lang="scss" scoped>
</style>
