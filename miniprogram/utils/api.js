// utils/api.js - API 请求封装
const app = getApp()

const request = (url, data, method = 'POST') => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.apiBaseUrl + url,
      method: method,
      data: data,
      timeout: 10000,
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          wx.showToast({ title: res.data?.detail || '请求失败', icon: 'none', duration: 3000 })
          reject(res.data)
        }
      },
      fail: (err) => {
        wx.showToast({ title: '网络异常：' + (err.errMsg || '请确认后端已启动'), icon: 'none', duration: 3000 })
        reject(err)
      }
    })
  })
}

module.exports = {
  parseConfig: (text) => request('/parse-config', { text }),
  calculatePrice: (config) => request('/calculate-price', { config }),
  submitLead: (data) => request('/submit-lead', data),
}
