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
// 获取所有关键词

export function getAllKeyword(params) {
    return request({
        url: '/get/offer/keyword/',
        method: 'get',
        params
    })
}
// 获取cpc 所有关键词

export function getCpckeyword(data) {
    return request({
        url: '/post/offer/keyword/cpc/',
        method: 'post',
        data
    })
}

// 获取类目信息

export function getAdgropInfo(params) {
    return request({
        url: '/get/campaign/adgroup/info/',
        method: 'get',
        params
    })
}

// 上传关键词

export function updata(data) {
    return request({
        url: '/post/mysql/keyword/',
        method: 'post',
        data
    })
}
