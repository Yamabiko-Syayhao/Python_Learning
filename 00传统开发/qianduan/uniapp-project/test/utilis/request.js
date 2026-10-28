// 接口基准地址，见《海南残联接口文档》1.1 API V1 接口说明
export const baseUrl = 'http://joint.byesame.com'

/**
 * 统一请求封装：自动拼接接口前缀
 * @param {Object} options uni.request 的配置项，url 传相对路径即可
 */
export const request = (options = {}) => {
	// uni.request 调接口的
	return uni.request({
		...options,
		url: /^https?:\/\//.test(options.url) ? options.url : baseUrl + options.url
	})
}
// 导出了一个名字叫request的函数 形参是options 默认值是空对象 
// 将来如何调用request({url:"/login",....})