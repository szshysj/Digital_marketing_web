<template>
  <div class="titleConten">
    <el-checkbox
      v-model="checkAll"
      class="titleLeft"
      :indeterminate="isIndeterminate"
      @change="handleCheckAllChange"
    >{{ areaName }}</el-checkbox>

    <el-checkbox-group v-model="checkedCities" class="titleRight" @change="handleCheckedCitiesChange">
      <el-checkbox
        v-for="(city,index) in cities"
        :key="index"
        :label="city.areaId"
        @change="abss(city.areaId)"
      >{{ city.areaName }}</el-checkbox>
    </el-checkbox-group>
  </div>
</template>

<script>
// const cityOptions = ['上海', '北京', '广州', '深圳']
export default {
    props: { 'areaName': {
        type: String,
        required: true
    }, 'areaChildr': {
        type: Array,
        required: true
    }, 'checkAlls': {
        type: Boolean,
        required: true
    }},
    data() {
        return {
            checkAll: true,
            dataAll: [],
            checkedCities: [],
            cities: this.areaChildr,
            isIndeterminate: false,
            removeIds: null
        }
    },
    computed: {},
    watch: {
        checkAlls(newdata, olddata) {
            if (newdata) {
                this.checkAll = true
            } else {
                this.checkAll = false
            }
            this.checkedCities = newdata ? this.dataAll : []
            this.isIndeterminate = false
        }
        // isIndeterminate(newdata, olddata) {
        //     this.$emit('checkData', {
        //         Indeterminate: newdata,
        //         remorIds: this.removeIds
        //     })
        // }
    },
    created() {
        const checkAreaAll = []
        const datachildr = this.areaChildr
        for (let i = 0; i < datachildr.length; i++) {
            checkAreaAll.push(datachildr[i].areaId)
        }
        this.checkedCities = checkAreaAll
        this.dataAll = checkAreaAll
    },
    methods: {
    // 地域选择
        handleCheckAllChange(val) {
            if (val) {
                this.checkedCities = this.dataAll
                this.$emit('checkData', {
                    Indeterminate: false,
                    remorIds: this.dataAll
                })
            } else {
                // console.log('开')
                this.checkedCities = []
                this.$emit('checkData', {
                    Indeterminate: true,
                    remorIds: this.dataAll
                })
            }
            // this.checkedCities = val ? this.dataAll : [];
            this.isIndeterminate = false
        },
        handleCheckedCitiesChange(value) {
            // const removeId = [...this.dataAll, ...value]
            // const dataAll = JSON.stringify(this.dataAll.sort())
            // const checkData = JSON.stringify(value.sort())
            // if (dataAll === checkData) {
            //     // console.log("相等");
            //     this.removeIds = value
            //     this.$emit('checkData', { Indeterminate: true, remorIds: value })
            // } else {
            //     // console.log("未选择");
            //     const d = new Set(removeId)
            //     const e = Array.from(d)
            //     const f = [
            //         ...e.filter(_ => !this.dataAll.includes(_)),
            //         ...e.filter(_ => !value.includes(_))
            //     ]
            //     // console.log(f);
            //     this.removeIds = f
            //
            // }
            const checkedCount = value.length
            this.checkAll = checkedCount === this.cities.length
            this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.cities.length
        },
        abss(value) {
            this.$emit('checkData', { Indeterminate: true, remorIds: [value] })
        }
    }
}
</script>

<style lang="scss" scoped>
.titleConten{
    .titleLeft{
        float: left;
        margin-right:100px
    }
    .titleRight{
        float: left
    }
    &::after{
        display: block;
        content: "";
        clear: both;
    }
}
</style>
