// pages/result/result.js
Page({
  data: {
    items: [],
    totalPrice: 0,
    unrecognized: []
  },

  onShow() {
    const app = getApp()
    const priceResult = app.globalData.priceResult
    const parsedConfig = app.globalData.parsedConfig

    if (!priceResult || !parsedConfig) {
      wx.showToast({ title: '暂无数据，请重新估价', icon: 'none' })
      wx.navigateBack()
      return
    }

    const items = priceResult.items || []
    const total = priceResult.total || 0

    // 检查未识别的硬件类别
    // 判断逻辑：解析器识别出了某个类别，但价格引擎未在库中找到对应价格的，才算未识别
    const unrecognized = []
    const categoryMap = { cpu: 'CPU', gpu: 'GPU', ram: '内存', ssd: '固态硬盘', hdd: '机械硬盘' }
    for (const [key, label] of Object.entries(categoryMap)) {
      const parsed = parsedConfig[key]
      if (parsed) {
        const found = items.some(item => item.name === label && item.price > 0)
        if (!found) {
          unrecognized.push({ key, label })
        }
      }
    }

    this.setData({
      items,
      totalPrice: total,
      unrecognized
    })
  },

  onRecycle() {
    wx.navigateTo({ url: '/pages/lead/lead' })
  },

  onBack() {
    wx.navigateBack()
  }
})
