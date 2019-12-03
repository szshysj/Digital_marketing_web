import request from '@/utils/request'

// 获取分词后的关键词列表
export function analyizerResult(params) {
    return request({
        url: '/get/analyizer/result/',
        method: 'get',
        params
    })
}

// 添加关键词

export function offerkeyword(data) {
    return request({
        url: '/post/offer/keyword/',
        method: 'post',
        data
    })
}
