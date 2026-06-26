// pages/lead/lead.js
const api = require('../../utils/api')

Page({
  data: {
    canSubmit: false,
    phone: '',
    wechat: '',
    totalPrice: 0,
    configPreview: '',
    showSuccess: false
  },

  onShow() {
    const app = getApp()
    const priceResult = app.globalData.priceResult
    const parsedConfig = app.globalData.parsedConfig

    if (!priceResult || !parsedConfig) {
      wx.showToast({ title: '请先估价', icon: 'none' })
      wx.navigateBack()
      return
    }

    // 构建配置预览文字
    const parts = []
    if (parsedConfig.cpu) parts.push('CPU: ' + parsedConfig.cpu)
    if (parsedConfig.gpu) parts.push('GPU: ' + parsedConfig.gpu)
    if (parsedConfig.ram) parts.push('内存: ' + parsedConfig.ram)
    if (parsedConfig.ssd) parts.push('SSD: ' + parsedConfig.ssd)
    if (parsedConfig.hdd) parts.push('HDD: ' + parsedConfig.hdd)
    const preview = parts.join(' | ')

    this.setData({
      totalPrice: priceResult.total || 0,
      configPreview: preview
    })
  },

  onPhoneInput(e) {
    const val = e.detail.value
    this.setData({ phone: val, canSubmit: val.trim().length > 0 })
  },

  onWechatInput(e) {
    this.setData({ wechat: e.detail.value })
  },

  async onSubmit() {
    const phone = this.data.phone.trim()

    // 简单手机号校验
    if (!phone || phone.length < 11) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' })
      return
    }
    if (!/^1\d{10}$/.test(phone)) {
      wx.showToast({ title: '手机号格式不正确', icon: 'none' })
      return
    }

    wx.showLoading({ title: '提交中...' })

    try {
      const app = getApp()
      const configText = app.globalData.configText || ''
      const parsedConfig = app.globalData.parsedConfig || {}
      const priceResult = app.globalData.priceResult || {}

      const res = await api.submitLead({
        phone: phone,
        wechat: this.data.wechat.trim(),
        config_text: configText,
        config_parsed: JSON.stringify(parsedConfig),
        price_total: priceResult.total || 0
      })

      wx.hideLoading()

      if (res.success) {
        this.setData({ showSuccess: true })
      } else {
        wx.showToast({ title: res.message || '提交失败', icon: 'none' })
      }
    } catch (err) {
      wx.hideLoading()
      console.error('提交失败:', err)
    }
  },

  onDone() {
    // 返回首页
    wx.switchTab({
      url: '/pages/index/index',
      fail: () => {
        // 如果没有 tabBar，用 navigateBack
        wx.navigateBack({ delta: 2 })
      }
    })
  }
})
