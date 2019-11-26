<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div>测试</div>
    <button @click="clickmi">测试接口</button>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: 'Dashboard',
    computed: {
        ...mapGetters(['name'])
    },
    methods: {
        clickmi() {
            this.$axios({
                method: 'get',
                url: '/apibj11x5.json'
                // url: '/api2/campaign/listCampaignNew.html?queryType=1&_page_csrf_token=1574646082457&_page_user_token='
                // headers: { 'JSESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImIyYi0yMjAxNDIxNzE4NjgzMjhmNDAiLCJleHAiOjE1NzI1MDk3NDl9.QT7BqvYLZ0TdglE3InJPdRm-qyeCTBQ11pNRq5MdTco' }
                // headers: { 'Cookie': 'cna=+EJIFloi9hECAXd7HJJNCIPf; UM_distinctid=16e3e637d14b17-0f75555eaf9722-b363e65-1fa400-16e3e637d1559e; ali_apache_id=11.186.201.38.1573004736426.367689.2; taklid=27b4df8483934e9aa99ce4f45c391744; ali_beacon_id=219.133.159.63.1573090760903.467404.0; ali_ab=219.133.159.63.1573093384999.6; lid=%E7%A2%A7%E8%BF%AA%E9%A3%9F%E5%93%81%E5%95%86%E8%A1%8C; ali_apache_track=c_mid=b2b-220142171868328f40|c_lid=%E7%A2%A7%E8%BF%AA%E9%A3%9F%E5%93%81%E5%95%86%E8%A1%8C|c_ms=2|c_mt=2; _m_h5_tk=557336b9c18bde903e8b3ead43e5433a_1574166763536; _m_h5_tk_enc=c149c149e3b4ccf9231eaa51b60c1742; __last_loginid__=%E7%A2%A7%E8%BF%AA%E9%A3%9F%E5%93%81%E5%95%86%E8%A1%8C; cookie2=1987022b62202f52f7b58f12abb5e73b; t=9a196f5a8ce53732171a3d71832a3db9; _tb_token_=37be173310ab0; alicnweb=lastlogonid%3D%25E7%25A2%25A7%25E8%25BF%25AA%25E9%25A3%259F%25E5%2593%2581%25E5%2595%2586%25E8%25A1%258C%7Ctouch_tb_at%3D1574394570728; csg=4c3240ac; uc4=nk4=0%400Dj2odzmENknMAStNds8b5ohhRmERxA%3D&id4=0%40U2grEJGHsQVv87c52869naTAbVtHQ25V; __cn_logon__=true; __cn_logon_id__=%E7%A2%A7%E8%BF%AA%E9%A3%9F%E5%93%81%E5%95%86%E8%A1%8C; ali_apache_tracktmp=c_w_signed=Y; _csrf_token=1574394584862; ctoken=tsPPBgRbd1R9zjkJ1tymcoco; lego_inform_timestamp=1574394598792; l=dBrd1CsuqCwqSSftBOCi5uI8aN_OSIRAguPRwNfMi_5Cq6Y1HaQOkd2Q9Fv6VjWfTZYB4NSLztv9-etkiD8Zf5GO_nhSNxDc.; isg=BNbWfyOOl3oa6qPEFcU4jnFjJ4wY3xq8q60rlUA_wrlUA3adqAdqwTzxn99KqxLJ' }
            }).then(res => {
                console.log(res)
            }).catch(err => {
                console.log(err)
                alert(err.response.data.cookie2)
            })
        }
    }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
