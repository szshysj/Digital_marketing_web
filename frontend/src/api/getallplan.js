import request from '@/utils/request'

// 获取所以计划
export function campaign(params) {
    return request({
        url: '/get/campaign/',
        method: 'get',
        params
    })
}

// 获取推广单元
export function campaignAdgroup(params) {
    return request({
        url: '/get/campaign/adgroup/',
        method: 'get',
        params
    })
}

// 所有推广单元详细信息

export function campaignAdgroupInfo(params) {
    return request({
        url: '/get/campaign/adgroup/info/',
        method: 'get',
        params
    })
}

// 删除推广计划
export function deletecampaign(params) {
    return request({
        url: '/delete/campaign/',
        method: 'get',
        params
    })
}
// 删除推广单元

export function deleteAdgroupsInfo(data) {
    return request({
        url: '/delete/adgroup/',
        method: 'POST',
        data
    })
}
