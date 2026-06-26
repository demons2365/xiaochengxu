// pages/index/index.js
const api = require('../../utils/api')

Page({
  data: {
    configText: '',
    canEstimate: false
  },

  onInput(e) {
    this.setData({ configText: e.detail.value, canEstimate: e.detail.value.trim().length > 0 })
  },

  // 点击示例自动填充
  fillExample(e) {
    const text = e.currentTarget.dataset.text
    this.setData({ configText: text, canEstimate: true })
  },

  // 上传截图（占位）
  onUploadImage() {
    wx.showToast({
      title: 'OCR识别功能即将上线',
      icon: 'none',
      duration: 2000
    })
  },

  // 立即估价
  async onEstimate() {
    const text = this.data.configText.trim()
    if (!text) {
      wx.showToast({ title: '请输入电脑配置', icon: 'none' })
      return
    }

    wx.showLoading({ title: '正在识别配置...' })

    try {
      // 1. 解析配置
      const parsedConfig = await api.parseConfig(text)

      // 检查是否解析出任何内容
      const hasContent = parsedConfig.cpu || parsedConfig.gpu || parsedConfig.ram || parsedConfig.ssd || parsedConfig.hdd
      if (!hasContent) {
        wx.hideLoading()
        wx.showToast({ title: '未能识别到硬件信息，请补充更多描述', icon: 'none' })
        return
      }

      // 2. 计算价格
      const priceResult = await api.calculatePrice(parsedConfig)

      // 3. 存储到全局
      const app = getApp()
      app.globalData.parsedConfig = parsedConfig
      app.globalData.priceResult = priceResult
      app.globalData.configText = text

      wx.hideLoading()

      // 4. 跳转到结果页
      wx.navigateTo({ url: '/pages/result/result' })

    } catch (err) {
      wx.hideLoading()
      wx.showToast({ title: '请求失败：' + (err.errMsg || '请确认后端已启动'), icon: 'none', duration: 3000 })
      console.error('估价失败:', err)
    }
  }
})
