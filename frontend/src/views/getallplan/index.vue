<template>
  <div class="app-container">
    <!-- header -->
    <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.importance" placeholder="Imp" clearable style="width: 90px" class="filter-item">
        <el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        下载
      </el-button>
      <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox>
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
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Date" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.strGMTCreate }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Title" min-width="150px">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          <!-- <el-tag>{{ row.type | typeFilter }}</el-tag> -->
        </template>
      </el-table-column>
      <el-table-column label="Author" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.state }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showReviewer" label="Reviewer" width="110px" align="center">
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
      <el-table-column label="Actions" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Edit
          </el-button>
          <el-button v-if="row.status!='published'" size="mini" type="success" @click="handleModifyStatus(row,'published')">
            Publish
          </el-button>
          <el-button v-if="row.status!='draft'" size="mini" @click="handleModifyStatus(row,'draft')">
            Draft
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleModifyStatus(row,'deleted')">
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

</template>

<script>
import { campaign } from '@/api/getallplan'
export default {
    data() {
        return {
            tableKey: 0, // 新增列表格
            listQuery: {// 双向数据绑定
                page: 1,
                limit: 20,
                importance: undefined,
                title: undefined,
                type: undefined,
                sort: '+id'
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
            list: null // 总数据
        }
    },
    created() {
        this.getList()
    },
    methods: {
        // 获取数据
        getList() {
            console.log('我是数据')
            campaign().then(res => {
                console.log(res)
                const data = res.data.data.campaignVOList
                this.list = data
                console.log(data, data.length)
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
        }
    }
}
</script>

<style lang="scss" scoped>

</style>
