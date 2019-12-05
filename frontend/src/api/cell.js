import request from '@/utils/request'

// 获取所以计划
export function campaign(params) {
    return request({
        url: '/get/campaign/',
        method: 'get',
        params
    })
}

// 获取所有商品
export function getparts(params) {
    return request({
        url: '/get/offer/',
        method: 'get',
        params
    })
}

// 添加选中的商品
export function addCampaign(data) {
    return request({
        url: '/post/adgroup/',
        method: 'post',
        data
    })
}
