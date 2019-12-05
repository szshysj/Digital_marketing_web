<template>
  <div class="app-container">
    <!-- header -->
    <div class="filter-container">
      <!-- <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" /> -->
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-upload2" @click="cell_campaign">
        加入计划
      </el-button>
    </div>
    <!-- content -->
    <el-table
      ref="multipleTable"
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
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
        :selectable="selectInit"
      />
      <!-- :selectable='selectInit' 选择禁用状态-->
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

      <el-table-column label="是否已经加入计划" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.isInCampaign === 1 ? '已加入':'否' }}</span>
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
    <div class="block">
      <span class="demonstration"><br></span>
      <el-pagination
        background
        :current-page="currentPage4"
        layout="total, prev, pager, next"
        :total="totals"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { getparts, addCampaign } from '@/api/cell' // api
import { campaignAdgroup, campaignAdgroupInfo } from '@/api/getallplan' // api
export default {
    // components: { Pagination },
    data() {
        return {
            selectedNumber: '', // 选中时获取的数组
            currentPage4: 1, // 默认第几页
            totals: 100, // 总页数
            tableKey: 0, // 新增列表格
            skip: 1, // 查询第几页
            options: {
                '1': '推广中',
                '-1': '手动暂停',
                '6': '不在投放时间下线，自动暂停'
            },
            listQuery: {// 双向数据绑定
                page: 1,
                limit: 10,
                importance: undefined,
                title: undefined,
                type: undefined,
                sort: 'page'
            },
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
        // 获取所有的商品
        get_cell() {
            let id = this.$route.query.id
            this.campaignId = id
            let parts_value = {}
            parts_value['skip'] = this.skip
            parts_value['campaignId'] = this.campaignId
            console.log('获取推广单元1')
            getparts(parts_value).then((res) => {
                console.log(res.data.data.promoteOfferList)
                console.log('获取推广单元')
                const dataok = res.data.data.promoteOfferList
                const dataok2 = res.data.data
                this.totals = dataok2.totalCount // 获取商品总数
                this.list = dataok
                // this.total = dataok.length
                this.listLoading = false
            }).catch(err => {
                console.log(err.response)
                alert('获取cpc失败')
            })
        },
        // 将选中商品加入计划内
        cell_campaign() {
            let add_cells = {}
            add_cells['campaignId'] = this.campaignId
            add_cells['b2bOfferIds'] = this.selectedNumber
            console.log(add_cells)
            addCampaign(add_cells).then(() => {
                alert('添加成功')
                this.get_cell()
            }).catch((err) => {
                console.log(err.response)
            })
        },
        // 分页1-每页多少条
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`)
        },
        // 分页1-当前页
        handleCurrentChange(val) {
            this.skip = val
            this.get_cell()
            console.log(`当前页: ${val}`)
        },
        // 选择禁用状态
        selectInit(row, index) {
            if (row.isInCampaign === 1) {
                return false
            } else {
                return true
            }
        },
        // 搜索事件
        // handleFilter() {
        //     this.listQuery.page = 1
        //     this.getList()
        // },
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
            this.selectedNumber = val
            this.selectedNumber = this.selectedNumber.map(list => {
                return list.offerId
            })
            this.selectedNumber = this.selectedNumber.join(',')
        }
    }
}
</script>

<style lang="scss" scoped>
</style>
