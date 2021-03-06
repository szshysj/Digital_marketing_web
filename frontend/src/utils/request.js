import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
    baseURL: 'http://120.77.183.17:8888', // 'http://120.77.183.17:8888',//process.env.VUE_APP_BASE_API, //'http://127.0.0.1:3000',// url = base url + request url
    // withCredentials: true, // send cookies when cross-domain requests
    timeout: 5000 // request timeout
    // headers: { 'JSESSION': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ImIyYi0yMjAxNDIxNzE4NjgzMjhmNDAiLCJleHAiOjE1NzI1MDk3NDl9.QT7BqvYLZ0TdglE3InJPdRm-qyeCTBQ11pNRq5MdTco' }
})

// 添加请求拦截器

service.interceptors.request.use(function(config) {
    // 在发送请求之前做些什么
    // config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    // console.log(config.headers['ddd'] = '666')

    let token = getToken()
    if (token) {
        token = (new Function('return (' + token + ')'))()
        if (config.method === 'post') {
            config.data = {
                ...config.data,
                'csrf_token': token.csrf_token,
                'cookie2': token.cookie2
            }
        } else if (config.method === 'get') {
            config.params = {

                'csrf_token': token.csrf_token,
                'cookie2': token.cookie2,
                ...config.params
            }
        }
    }

    return config
}, function(error) {
    // 对请求错误做些什么
    return Promise.reject(error)
})

// 添加响应拦截器
service.interceptors.response.use(function(response) {
    // 对响应数据做点什么
    return response
}, function(error) {
    // 对响应错误做点什么
    const status = error.response.status
    const errdata = error.response.data
    if (status == 401) {
        let errText = []
        for (let item in errdata) {
            errText.push(errdata[item])
        }
        errText = errText.join('\n')
        MessageBox.confirm(errText, {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'error'
        }).then(() => {
            store.dispatch('user/resetToken').then(() => {
                location.reload()
            })
        })
        return Promise.reject(error.response.data)
    } else if (status == 404) {
        let errText = []
        for (let item in errdata) {
            errText.push(errdata[item])
        }
        errText = errText.join('\n')
        Message.error(errText)
        return Promise.reject(error.response)
    } else if (status >= 500) {
        return Promise.reject('服务器错误！！！')
    }

    return Promise.reject(error.response)
})

// request interceptor
// service.interceptors.request.use(
//     config => {
//         // do something before request is sent

//         if (store.getters.token) {
//             // let each request carry token
//             // ['X-Token'] is a custom headers key
//             // please modify it according to the actual situation
//             config.headers['X-Token'] = getToken()
//         }
//         return config
//     },
//     error => {
//         // do something with request error
//         console.log(error) // for debug
//         return Promise.reject(error)
//     }
// )

// response interceptor
// service.interceptors.response.use(
//     /**
//      * If you want to get http information such as headers or status
//      * Please return  response => response
//     */

//     /**
//      * Determine the request status by custom code
//      * Here is just an example
//      * You can also judge the status by HTTP Status Code
//      */
//     response => {
//         const res = response.data

//         // if the custom code is not 20000, it is judged as an error.
//         if (res.code !== 20000) {
//             Message({
//                 message: res.message || 'Error',
//                 type: 'error',
//                 duration: 5 * 1000
//             })

//             // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
//             if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
//                 // to re-login
//                 MessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
//                     confirmButtonText: 'Re-Login',
//                     cancelButtonText: 'Cancel',
//                     type: 'warning'
//                 }).then(() => {
//                     store.dispatch('user/resetToken').then(() => {
//                         location.reload()
//                     })
//                 })
//             }
//             return Promise.reject(new Error(res.message || 'Error'))
//         } else {
//             return res
//         }
//     },
//     error => {
//         console.log('err' + error) // for debug
//         Message({
//             message: error.message,
//             type: 'error',
//             duration: 5 * 1000
//         })
//         return Promise.reject(error)
//     }
// )

export default service
