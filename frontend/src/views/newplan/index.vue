<template>
  <div class="app-container">
    <el-form ref="form" :model="form" :rules="rules" label-width="120px" status-icon>
      <el-form-item label="计划名称：" prop="name">
        <el-input v-model="form.name" placeholder="计划创建于_20191030_020027" class="input-widht" />
      </el-form-item>
      <el-form-item label="消耗上线：" prop="quota">
        <el-input v-model.number="form.quota" class="input-widht" />
        <span>元 / 天</span>
      </el-form-item>
      <el-form-item label="推广时段：">
        <el-button type="text" @click="Timelot = true">时段设置</el-button>
        <el-dialog title="请选择时间端" :visible.sync="Timelot" width="30%" :before-close="handleClose">
          <span>这是一段信息</span>
          <span slot="footer" class="dialog-footer">
            <el-button @click="Timelot = false">取 消</el-button>
            <el-button type="primary" @click="Timelot = false">确 定</el-button>
          </span>
        </el-dialog>
      </el-form-item>
      <el-form-item label="推广地域：">
        <el-button type="text" @click="region = true">地域设置</el-button>
        <el-dialog title="请选择地域" :visible.sync="region" width="30%" :before-close="handleClose">
          <span>这是一段信息</span>
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
          <i></i>
        </el-tooltip>

        <el-switch v-model="form.directional"></el-switch>
        <span>已开启</span>
      </el-form-item>
      <el-form-item class="foot-success">
        <el-col :span="11" class="col-left">
          <el-checkbox v-model="checkboxs"></el-checkbox>
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
import { getdata } from "@/api/newplan";
import afteri from "@/assets/imgs/after-i.png";
export default {
  data() {
    return {
      Timelot: false,
      region: false,
      checkboxs: false,
      form: {
        mane: "",
        quota: 100,
        directional: true
      },
      rules: {
        name: [
          { required: true, message: "请输入计划名称", trigger: "blur" },
          { min: 1, max: 40, message: "长度在 1 到 40 个字符", trigger: "blur" }
        ],
        quota: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" }
        ]
      }
    };
  },
  created() {
    //console.log(this);
    getdata().then(res => {
      console.log(res);
    });
  },
  methods: {
    onSubmit() {
      this.$message("提交成功!");
    },
    onCancel() {
      this.$message({
        message: "cancel!",
        type: "warning"
      });
    },
    handleClose(done) {
      this.$confirm("确认关闭？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(_ => {
          done();
        })
        .catch(_ => {});
    }
  }
};
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
</style>