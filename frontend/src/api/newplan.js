import request from '@/utils/request'

export function getdata(params) {
    return request({
        url: '/get/area/',
        method: 'get',
        params
    })
}
