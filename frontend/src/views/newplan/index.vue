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
          <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate">全选</el-checkbox>
          <div v-for="(item, index) in datas" :key="index">
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

        <el-switch v-model="form.directional" @click="cositeFlag" />
        <span>已开启</span>
      </el-form-item>
      <el-form-item class="foot-success">
        <el-col :span="11" class="col-left">
          <el-checkbox v-model="checkboxs" />
          <a target="_blank">《智能营销软件服务协议》</a>
          <a target="_blank">《营效宝软件服务协议》</a>
          <a target="_blank">《广告服务协议》</a>
        </el-col>
        <el-col :span="11">
          <el-button type="primary" @click="onSubmit">确认提交</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getdata } from '@/api/newplan'
import regions from '@/components/Newplan/region'
export default {
    components: {
        regions
    },
    data() {
    // 名称匹配规则
        const validatename = (rule, value, callback) => {
            const strs = value.split(' ').join('').length

            console.log(value)

            if (strs == 0) {
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
            console.log(value)
            if (value === '' || value === undefined) {
                callback(new Error('请输入预算价格'))
            } else if (value < 60 || value > 999999) {
                callback(new Error('价格在60-999999之间'))
            } else {
                callback()
            }
        }

        return {
            Timelot: false,
            region: false,
            datas: null,
            isIndeterminate: false,
            checkAll: true,
            checkboxs: false,
            regionId: null,

            form: {
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
    created() {
    // console.log(this);
        getdata()
            .then(res => {
                const Data = res.data.areas
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
            })
            .catch(error => {
                console.log(error)
            })
    },
    methods: {
    // 表单提交
        onSubmit() {
            this.$message('提交成功!')
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
        // 接收子组件传值
        checkData(res) {
            console.log(res)
            const okId = []
            if (this.regionId.length == 35) {
                this.isIndeterminate = res.Indeterminate
            }
            function concatData(arrA, arrB) {
                console.log(arrA, arrB)
                const concatD = arrA.concat(arrB)
                const json = {}
                const dataId = []
                for (let i = 0; i < concatD.length; i++) {
                    if (!json[concatD[i]]) {
                        json[concatD[i]] = concatD[i]
                    }
                }

                for (const item in json) {
                    dataId.push(item)
                }
                console.log(dataId)
                // return result;
            }
            const ok = concatData(this.regionId, res.remorIds)
            // this.regionId = [...ok];
            console.log(ok)
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
</style>
