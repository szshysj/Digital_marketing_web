import request from '@/utils/request'

export function getdata(params) {
    return request({
        url: '/getApi',
        method: 'get',
        params
    })
}
