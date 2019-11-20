import request from '@/utils/request'

export function getdata(params) {
    return request({
        url: '/get/area/',
        method: 'get',
        params
    })
}

export function postcampaign(params) {
    return request({
        url: '/post/add/campaign/',
        method: 'POST',
        data: params
    })
}
