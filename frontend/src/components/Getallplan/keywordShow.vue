<template>
  <div>
    <template v-if="showPc">
      {{ onPcPv() }}<span class="spanClick" @click="showUpdata(row,'show','pc')">编辑</span>
    </template>
    <template v-else>
      <el-input v-model.trim="value" class="inputWidth" />
      <el-button type="success" @click="showUpdata(row, 'off','pc')">确定</el-button>
      <span class="offSpan" @click="offShow">取消</span>
    </template>
  </div>
</template>

<script>
export default {
    props: {
        'row': {
            type: Object,
            required: true
        },
        'offpc': {
            type: String,
            required: true
        }
    },
    data() {
        return {
            showPc: true, // 控制pc
            value: ''
        }
    },
    created() {
        this.value = this.onPcPv()
    },
    methods: {
        // 编辑价格
        showUpdata(row, res, offP) {
            if (res == 'show') {
                this.showPc = false
            } else {
                let value = this.value
                let reg = /^[0-9]+.?[0-9]*$/ // 判断字符串是否为数字 ，判断正整数用/^[1-9]+[0-9]*]*$/
                if (!reg.test(value)) {
                    this.$message.error('错了哦!输入数字')
                } else {
                    this.showPc = true
                    // 后期需要优化
                    if (this.offpc == 'pc') {
                        row.pc = value
                    } else {
                        row.pv = value
                    }
                }
            }
        },
        // 取消
        offShow() {
            this.showPc = !this.showPc
        },
        // 四舍五入
        rounding(value) {
            let vas = parseFloat(value)
            return vas.toFixed(1)
        },
        // 判断pc还是pv
        onPcPv() {
            if (this.offpc == 'pc') {
                return this.rounding(this.row.pc)
            } else {
                return this.rounding(this.row.pv)
            }
        }

    }
}
</script>

<style lang="scss" scoped>
.spanClick{
    font-size: 16px;
    color: #409EFF;
    cursor: pointer;
}
.inputWidth{
    width: 150px
}
.offSpan{
    cursor: pointer;
    color: #F56C6C
}
</style>
