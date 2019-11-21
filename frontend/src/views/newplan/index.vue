<template>
  <div class="app-container">
    <el-form ref="form" :model="form" :rules="rules" label-width="120px" status-icon>
      <el-form-item label="计划名称：" prop="name">
        <el-input v-model.trim="form.name" placeholder="计划创建于_20191030_020027" class="input-widht" />
      </el-form-item>
      <el-form-item label="消耗上线：" prop="quota">
        <el-input v-model.number="form.quota" class="input-widht" />
        <span>元 / 天</span>
      </el-form-item>
      <el-form-item label="推广时段：">
        <el-button type="text" @click="Timelot = true">时段设置</el-button>
        <el-dialog title="请选择时间端" :visible.sync="Timelot" width="35%" :before-close="handleClose">
          <div class="time-tips">
            <span>全天: 7*24小时</span>
            <span>闲时: 晚上9点到早上6点</span>
            <span>热门时间段: 上午10点到12点 - 下午3点到6点 - 晚上9点到11点</span>
          </div>
          <div class="time-check">
            <el-radio-group v-model="form.radio" class="check-box">
              <el-radio
                v-for="(item,index) in schedule_dict"
                :key="index"
                :label="index+1"
              >{{ item.target_name }}</el-radio>
            </el-radio-group>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button @click="Timelot = false">取 消</el-button>
            <el-button type="primary" @click="Timelot = false">确 定</el-button>
          </span>
        </el-dialog>
      </el-form-item>
      <el-form-item label="推广地域：">
        <el-button type="text" @click="region = true">地域设置</el-button>
        <el-dialog title="请选择地域" :visible.sync="region" width="45%" :before-close="handleClose">
          <div class="headerTile">
            <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="quanxuan">全选</el-checkbox>
            <span>省份</span>
          </div>

          <div v-for="(item, index) in datas" :key="index">
            <!-- areaName:大地区，childr：大地区中的小地区, checkAll：是否全选-->
            <regions
              :area-name="item.areaName"
              :area-childr="item.childr"
              :check-alls="checkAll"
              @checkData="checkData"
            />
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button @click="region = false">取 消</el-button>
            <el-button type="primary" @click="region = false">确 定</el-button>
          </span>
        </el-dialog>
      </el-form-item>
      <el-form-item label="定向推广" prop="directional" class="after-img">
        <el-tooltip class="item" effect="dark" placement="bottom">
          <div
            slot="content"
            class="after-text"
          >站外定向推广，是1688站内推广资源的拓展和补充。营效宝将潜在买家流量引入到商家店铺商品详情页，所有参与外投的商品均有机会获得站外流量</div>
          <i />
        </el-tooltip>

        <el-switch v-model="form.directional" @change="cositeFlag" />
        <span>{{ cositeFlagText }}</span>
      </el-form-item>
      <el-form-item class="foot-success">
        <el-col :span="11" class="col-left">
          <el-checkbox v-model="checkboxs" />
          <a target="_blank">《智能营销软件服务协议》</a>
          <a target="_blank">《营效宝软件服务协议》</a>
          <a target="_blank">《广告服务协议》</a>
        </el-col>
        <el-col :span="11">
          <el-button type="primary" :disabled="disableds" @click="onSubmit">确认提交</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getdata, postcampaign } from '@/api/newplan'
import regions from '@/components/Newplan/region'
export default {
    components: {
        regions
    },
    data() {
    // 名称匹配规则
        const validatename = (rule, value, callback) => {
            if (value === '' || value === undefined) {
                callback(new Error('请输入计划名称'))
            } else if (maxstr(value) > 40) {
                callback(new Error('标题长度在1-40之间'))
            } else {
                callback()
            }

            // 处理汉字和字母长度
            function maxstr(str) {
                let realLength = 0
                const len = str.length
                let charCode = -1
                for (let i = 0; i < len; i++) {
                    charCode = str.charCodeAt(i)
                    if (charCode >= 0 && charCode <= 128) realLength += 1
                    else realLength += 2
                }
                return realLength
            }
        }
        // 预算价格匹配规则
        const validatequota = (rule, value, callback) => {
            if (value === '' || value === undefined) {
                callback(new Error('请输入预算价格'))
            } else if (value < 60 || value > 100) {
                callback(new Error('价格在60-100之间'))
            } else {
                callback()
            }
        }

        return {
            Timelot: false, // 弹出窗时间
            region: false, // 弹出窗地区
            datas: null, // 地区中数据
            isIndeterminate: false, // 全选样式
            checkAll: true, // 单个组件全选
            checkboxs: false, // 协议勾选
            regionId: null, // 总id数
            regionIdCont: null, // 备份总id
            disableds: false, // 阻止点击

            form: {// 表单数据
                mane: '',
                quota: 100,
                directional: true,
                radio: 1
            },
            rules: {
                name: [{ required: true, validator: validatename, trigger: 'blur' }],
                quota: [
                    { required: true, validator: validatequota, trigger: 'blur' },
                    { type: 'number', message: '必须为数字值' }
                ]
            },
            schedule_dict: [
                {
                    target_name: '7*24 全天',
                    1: '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
                },
                {
                    target_name: '7天 热门',
                    2: '000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110'
                },
                {
                    target_name: '7天 闲时',
                    3: '111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111'
                },
                {
                    target_name: '工作日 全天',
                    4: '000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000000000'
                },
                {
                    target_name: '工作日 热门',
                    5: '000000000000000000000000000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000000000011000111000110000000000000000000000000'
                },
                {
                    target_name: '工作日 闲时',
                    6: '000000000000000000000000111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111111111000000000000000111000000000000000000000000'
                },
                {
                    target_name: '休息日 全天',
                    7: '111111111111111111111111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111111111111111111111'
                },
                {
                    target_name: '休息日 热门',
                    8: '000000000011000111000110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011000111000110'
                },
                {
                    target_name: '休息日 闲时',
                    9: '111111000000000000000111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000111111000000000000000111'
                }
            ]
        }
    },
    // 计算属性
    computed: {
        cositeFlagText() {
            return this.form.directional ? '已开启' : '关闭'
        }
    },
    created() {
    // console.log(this);
        // getdata()
        //     .then(res => {

        //     })
        //     .catch(error => {
        //         console.log(error)
        //     })
        const Data = [{ 'areaId': 2610, 'parentId': 10042, 'areaName': '上海', 'areaType': 'province' }, { 'areaId': 10040, 'parentId': 10032, 'areaName': '东北地区', 'areaType': 'area' }, { 'areaId': 10032, 'areaName': '中国', 'areaType': 'country' }, { 'areaId': 3559, 'parentId': 10045, 'areaName': '云南', 'areaType': 'province' }, { 'areaId': 2434, 'parentId': 10041, 'areaName': '内蒙古', 'areaType': 'province' }, { 'areaId': 1098, 'parentId': 10041, 'areaName': '北京', 'areaType': 'province' }, { 'areaId': 10042, 'parentId': 10032, 'areaName': '华东地区', 'areaType': 'area' }, { 'areaId': 10043, 'parentId': 10032, 'areaName': '华中地区', 'areaType': 'area' }, { 'areaId': 10041, 'parentId': 10032, 'areaName': '华北地区', 'areaType': 'area' }, { 'areaId': 10044, 'parentId': 10032, 'areaName': '华南地区', 'areaType': 'area' }, { 'areaId': 4858, 'parentId': 10047, 'areaName': '台湾', 'areaType': 'province' }, { 'areaId': 2118, 'parentId': 10040, 'areaName': '吉林', 'areaType': 'province' }, { 'areaId': 3078, 'parentId': 10045, 'areaName': '四川', 'areaType': 'province' }, { 'areaId': 3256, 'parentId': 10041, 'areaName': '天津', 'areaType': 'province' }, { 'areaId': 2536, 'parentId': 10046, 'areaName': '宁夏', 'areaType': 'province' }, { 'areaId': 1002, 'parentId': 10042, 'areaName': '安徽', 'areaType': 'province' }, { 'areaId': 2847, 'parentId': 10042, 'areaName': '山东', 'areaType': 'province' }, { 'areaId': 2728, 'parentId': 10041, 'areaName': '山西', 'areaType': 'province' }, { 'areaId': 2614, 'parentId': 10044, 'areaName': '广东', 'areaType': 'province' }, { 'areaId': 1277, 'parentId': 10044, 'areaName': '广西', 'areaType': 'province' }, { 'areaId': 3371, 'parentId': 10046, 'areaName': '新疆', 'areaType': 'province' }, { 'areaId': 2177, 'parentId': 10042, 'areaName': '江苏', 'areaType': 'province' }, { 'areaId': 2258, 'parentId': 10042, 'areaName': '江西', 'areaType': 'province' }, { 'areaId': 1511, 'parentId': 10041, 'areaName': '河北', 'areaType': 'province' }, { 'areaId': 1670, 'parentId': 10043, 'areaName': '河南', 'areaType': 'province' }, { 'areaId': 3478, 'parentId': 10042, 'areaName': '浙江', 'areaType': 'province' }, { 'areaId': 1474, 'parentId': 10044, 'areaName': '海南', 'areaType': 'province' }, { 'areaId': 10000, 'areaName': '海外', 'areaType': 'country' }, { 'areaId': 10047, 'parentId': 10032, 'areaName': '港澳台', 'areaType': 'area' }, { 'areaId': 1908, 'parentId': 10043, 'areaName': '湖北', 'areaType': 'province' }, { 'areaId': 2002, 'parentId': 10043, 'areaName': '湖南', 'areaType': 'province' }, { 'areaId': 4853, 'parentId': 10047, 'areaName': '澳门', 'areaType': 'province' }, { 'areaId': 1181, 'parentId': 10046, 'areaName': '甘肃', 'areaType': 'province' }, { 'areaId': 1103, 'parentId': 10042, 'areaName': '福建', 'areaType': 'province' }, { 'areaId': 10046, 'parentId': 10032, 'areaName': '西北地区', 'areaType': 'area' }, { 'areaId': 10045, 'parentId': 10032, 'areaName': '西南地区', 'areaType': 'area' }, { 'areaId': 3290, 'parentId': 10045, 'areaName': '西藏', 'areaType': 'province' }, { 'areaId': 1382, 'parentId': 10045, 'areaName': '贵州', 'areaType': 'province' }, { 'areaId': 2361, 'parentId': 10040, 'areaName': '辽宁', 'areaType': 'province' }, { 'areaId': 3262, 'parentId': 10045, 'areaName': '重庆', 'areaType': 'province' }, { 'areaId': 2973, 'parentId': 10046, 'areaName': '陕西', 'areaType': 'province' }, { 'areaId': 2561, 'parentId': 10046, 'areaName': '青海', 'areaType': 'province' }, { 'areaId': 4846, 'parentId': 10047, 'areaName': '香港', 'areaType': 'province' }, { 'areaId': 1816, 'parentId': 10040, 'areaName': '黑龙江', 'areaType': 'province' }]
        const newData = []
        const pareD = []
        for (let i = 0; i < Data.length; i++) {
            if (Data[i].areaType == 'area') {
                pareD.push(Data[i])
            } else {
                if (Data[i].areaName == '中国') {
                    continue
                }
                newData.push(Data[i])
            }
        }
        // 整合
        const childr = []
        for (let i = 0; i < pareD.length; i++) {
            pareD[i].childr = []
            for (let j = 0; j < newData.length; j++) {
                if (pareD[i].areaId == newData[j].parentId) {
                    pareD[i].childr.push(newData[j])
                }

                if (
                    newData[j].areaName == '海外' &&
              pareD[i].areaName == '港澳台'
                ) {
                    pareD[i].areaName = '其他地区'
                    pareD[i].childr.push(newData[j])
                }
            }
        }

        const dataId = []
        newData.forEach((value, index) => {
            dataId.push(value.areaId)
        })
        this.datas = pareD
        this.regionId = dataId
        this.regionIdCont = dataId
    },
    methods: {
        // 表单提交
        onSubmit() {
            if (this.checkboxs) {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.disableds = true
                        let postCampaginJson = {}
                        postCampaginJson['title'] = this.form.name
                        postCampaginJson['budget'] = this.form.quota
                        postCampaginJson['cositeFlag'] = this.form.directional ? 1 : 0
                        postCampaginJson['promoteTime'] = this.form.radio
                        if (this.regionId.length == 35 || this.regionId.length == 0) {
                            postCampaginJson['promoteArea'] = '0'
                        } else {
                            postCampaginJson['promoteArea'] = this.regionId
                        }

                        postcampaign(postCampaginJson).then(res => {
                            console.log(res)
                            this.disableds = false
                            this.$refs.form.resetFields()
                            this.form.radio = 1
                            this.checkboxs = false

                            this.$message({
                                message: '恭喜你，提交成功',
                                type: 'success'
                            })
                        }).catch(err => {
                            console.log(err)
                            this.$message.error('错误！！！')
                        })
                    } else {
                        this.$message.error('请填写字段')
                        return false
                    }
                })
            } else {
                this.$message.error('请勾选协议')
            }
        },
        // 关闭弹出层
        handleClose(done) {
            this.$confirm('确认关闭？', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            })
                .then(_ => {
                    done()
                })
                .catch(_ => {})
        },
        // 定向推广
        cositeFlag(res) {
            if (!res) {
                this.form.directional = true

                this.$confirm('关闭“站外定向推广”功能后，该计划下推广信息的展现量和点击量都有可能减少，系统建议您开启该功能。确认关闭后，将在10分钟内生效。确认关闭吗？', '定向推广', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'

                }).then(() => {
                    this.form.directional = false
                }).catch(() => {
                    this.form.directional = true
                })
            }
        },
        // 接收子组件传值
        checkData(res) {
            // console.log(res)
            if (res.Indeterminate) {
                const regionId = this.regionId
                let okid = [...this.regionId]
                const remorIds = res.remorIds
                let delData = []
                for (let i = 0; i < regionId.length; i++) {
                    for (let j = 0; j < remorIds.length; j++) {
                        if (regionId[i] == remorIds[j]) {
                            delData.push(regionId[i])
                            okid.splice(i, 1)
                        }
                    }
                }
                let concatD = diff(remorIds, delData)

                // console.log(okid, 111)
                // console.log(concatD)
                if (res.remorIds.length > 1) {
                    let quanx1 = diff(regionId, res.remorIds)
                    this.regionId = quanx1
                    // console.log('3个')
                } else {
                    this.regionId = okid.concat(concatD)
                }

                // console.log('总', this.regionId)
            } else {
                let quanx = conCatData(this.regionId, res.remorIds)
                this.regionId = quanx
                // console.log(quanx)
            }

            function conCatData(arr1, arr2) {
                let a = [...arr1, ...arr2]
                // console.log(a)
                let b = new Set(a)
                let c = Array.from(b)
                return c
            }
            // 两个数组，相同去重
            function diff(arr1, arr2) {
                // console.log(arr1, arr2)
                let a = []
                let b = []
                for (let i = 0; i < arr2.length; i++) {
                    a[arr2[i]] = true
                }
                for (let i = 0; i < arr1.length; i++) {
                    if (!a[arr1[i]]) {
                        b.push(arr1[i])
                    }
                }
                // console.log(b)
                return b
            }

            if (this.regionId.length == 35 || this.regionId.length == 0) {
                this.isIndeterminate = false
            } else {
                this.isIndeterminate = true
            }
            // console.log('总', this.regionId)
            // function concatData(arrA, arrB) {
            //     console.log(arrA, arrB)
            //     const concatD = arrA.concat(arrB)
            //     const json = {}
            //     const dataId = []
            //     for (let i = 0; i < concatD.length; i++) {
            //         if (!json[concatD[i]]) {
            //             json[concatD[i]] = concatD[i]
            //         }
            //     }

            //     for (const item in json) {
            //         dataId.push(item)
            //     }
            //     console.log(dataId)
            //     // return result;
            // }
            // const ok = concatData(this.regionId, res.remorIds)
            // this.regionId = [...ok];
            // console.log(ok)
        },
        // 全选
        quanxuan(value) {
            if (value) {
                this.regionId = this.regionIdCont
                this.isIndeterminate = false
            } else {
                this.regionId = []
                this.isIndeterminate = false
            }
            console.log(this.regionId)
        }

    }
}
</script>

<style lang="scss" scoped>
.input-widht {
  width: 50%;
}
.after-img {
  i {
    position: absolute;
    width: 20px;
    height: 20px;
    background: url("~@/assets/imgs/after-i.png") no-repeat;
    background-size: cover;
    left: -39px;
    top: 25%;
  }
}
.after-text {
  width: 240px;
}
.foot-success {
  margin-top: 100px;
  .el-checkbox {
    margin: 0 0 0 20px;
  }
  a {
    color: #fc863f;
  }
  .col-left {
    background: #e8e8e8;
    border-radius: 4px;
  }
}
.time-tips {
  border-bottom: 1px solid #409eff;
  padding-bottom: 15px;
  span {
    display: block;
    line-height: 30px;
  }
}
.time-check {
  padding-top: 15px;
  .check-box {
    line-height: inherit;
  }
}
// 全选样式
.headerTile {
    span{
      margin-left: 92px;
      color: #409EFF;
    }
}
</style>
