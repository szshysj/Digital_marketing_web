import request from '@/utils/request'

export function campaign(params) {
    return request({
        url: '/get/campaign/',
        method: 'get',
        params
    })
}
