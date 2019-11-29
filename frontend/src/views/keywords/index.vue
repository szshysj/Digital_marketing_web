<template>
  <div>
    这是关键词
  </div>
</template>

<script>
export default {
    data() {
        return {

        }
    },
    created() {
        let title = this.$route.query.title
        console.log(title)
        alert(title)
    }
}
</script>

<style lang="scss" scoped>

</style>
