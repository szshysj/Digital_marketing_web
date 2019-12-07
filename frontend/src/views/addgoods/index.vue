<template>
  <div class="app-container">
    <!-- <el-button class="filter-item" :disabled="banif" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="open_delete_ids">
      删除单元
    </el-button> -->
    <!-- header class="filter-container"-->
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
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加单元
      </el-button>
      <el-button class="filter-item" :disabled="banif" style="margin-left: 10px;" type="danger" icon="el-icon-delete" @click="open_delete_ids">
        删除单元
      </el-button>
      <!-- <template>
        <el-button type="text" @click="open">点击打开 Message Box</el-button>
      </template> -->
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
      style="width: 100%; margin-top: 20px;"
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
      <!-- <el-table-column label="ID" prop="id" sortable="custom" align="center" width="80" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <el-checkbox :ids="row.id" />
        </template>
      </el-table-column> -->
      <el-table-column label="单元名称" width="250px" fixed="left">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
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
          <span>{{ row.category }}</span>
        </template>
      </el-table-column>

      <el-table-column label="关键词数" width="110px" align="center">
        <template slot-scope="{row}">
          <span style="color:red;">{{ row.keywordCount }}</span>
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

      <!-- <el-table-column label="Imp" width="80px">
        <template slot-scope="{row}">
          <span>{{ row.keywordMode }}</span>

        </template>
      </el-table-column>
      <el-table-column label="Readings" align="center" width="95">
        <template slot-scope="{row}">

          <span>{{ row.budget }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Status" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.status">
            {{ row.budget }}
          </el-tag>
        </template>
      </el-table-column> -->

      <!-- 按钮功能 -->
      <el-table-column label="Actions" align="center" width="180" class-name="small-padding fixed-width" fixed="right">
        <template slot-scope="{row}">
          <el-button type="success" size="mini" @click="goodsPlan(row)">
            关键字
          </el-button>
          <!-- <el-button type="primary" size="mini" @click="handleUpdate(row)">
            修改
          </el-button> -->
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="open_del_id(row)">
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
import { campaignAdgroup, campaignAdgroupInfo, deleteAdgroupsInfo } from '@/api/getallplan' // api
import Pagination from '@/components/Pagination' // 分页组件
export default {
    components: { Pagination },
    data() {
        return {
            banif: true,
            multipleSelection: {}, // 存放选中的值
            deleteId: {}, // 存放需要删除的id
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
            let id = this.$route.query.id
            let params = {}
            params['campaignId'] = id
            // 获取所有推广单元的id
            campaignAdgroup(params).then(res => {
                const dataLength = res.data.data.totalCount
                console.log(dataLength)
                if (dataLength > 0) {
                    const dataId = res.data.data.adGroupVOList
                    let jsonId = []
                    let dataArr = []
                    let dataStar = {}
                    for (let i = 0; i < dataId.length; i++) {
                        dataArr.push(dataId[i].id)
                    }
                    for (let i = 0; i < dataArr.length; i += 10) {
                        jsonId.push(dataArr.slice(i, i + 10))
                    }
                    // 整合数据，分页传多个id id == page
                    dataStar['adGroupIds'] = jsonId[this.listQuery.page - 1].join(',')
                    dataStar['limit'] = dataLength

                    // 获取所有推广单元详细信息
                    campaignAdgroupInfo(dataStar).then(res => {
                        const datares = res.data.data
                        const dataok = datares.adGroupVOList
                        this.list = dataok
                        this.total = dataLength
                    })
                }

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
        handleCreate(val) {
            // console.log('我是添加')
            // this.$message({
            //     message: '我是添加',
            //     type: 'success'
            // })
            let id = this.$route.query.id
            let params = {}
            params['campaignId'] = id
            const title = val.title
            // 将推广计划IP传入添加单元页面
            this.$router.push({ path: '/getallplan/addcell', query: { id: params.campaignId, title: title }})
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
            if (val.length > 0) {
                this.banif = false
            } else {
                this.banif = true
            }
            this.multipleSelection = val
            console.log(val)
            console.log(this.list)
        },
        // 修改标题
        handleUpdate(val) {
            console.log(val)
            // this.$confirm('我是修改计划', '修改', {
            //     confirmButtonText: '确定',
            //     cancelButtonText: '取消',
            //     type: 'warning'
            // }).then(() => {
            //     this.$message({
            //         type: 'success',
            //         message: '成功!'
            //     })
            // }).catch(() => {
            //     this.$message({
            //         type: 'info',
            //         message: '取消'
            //     })
            // })
        },
        // 多选删除
        delete_ids() {
            // this.deleteId = this.multipleSelection
            // let i = this.multipleSelection[0]
            if (this.multipleSelection[0]) {
                let dl_ids = this.multipleSelection.map(item => {
                    return item.id
                })
                this.deleteId['adGroupIds'] = dl_ids
                console.log(this.deleteId)
                // this.deleteId = this.deleteId.join(',')
                deleteAdgroupsInfo(this.deleteId).then(() => {
                    console.log('删除成功')
                })
                this.getList()
            } else {
                console.log('值为空')
            }
        },
        // 单个按钮删除
        del_id(val) {
            let dl_id = {}
            dl_id['adGroupIds'] = val.id
            deleteAdgroupsInfo(dl_id).then(() => {
                console.log('删除成功')
                this.getList()
            })
        },
        // 跳转推广单元关键词商品
        goodsPlan(val) {
            const title = val.title
            const campaignId = this.$route.query.id
            const adGroupIdList = val.id
            // console.log(goodsId, '我是推广单元商品跳转')

            this.$router.push({ path: '/getallplan/keywords', query: { title, campaignId, adGroupIdList }})
        },
        // 弹窗&多选删除
        open_delete_ids() {
            // let $this =this
            this.$confirm('此操作将删除所选商品, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                this.delete_ids()
                this.$message({
                    type: 'success',
                    message: '删除成功!',
                    duration: 1500
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除',
                    duration: 1500
                })
            })
        },
        // 弹窗&单按钮删除
        open_del_id(rows) {
            // let $this =this
            let row = rows // 接收参数
            this.$confirm('此操作将删除所选商品, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
                center: true
            }).then(() => {
                console.log('sanchu')
                this.del_id(row)
                this.$message({
                    type: 'success',
                    message: '删除成功!',
                    duration: 1500
                })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除',
                    duration: 1500
                })
            })
        }
    }
}
</script>

<style lang="scss" scoped>
.aa{
    font-family: 500
}
</style>
