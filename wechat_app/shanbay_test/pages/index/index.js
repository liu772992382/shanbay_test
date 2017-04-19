//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    finish: false
  },
  //加载页面
  onLoad: function () {
    var that = this
    console.log('index:load')
    this.setData({
      userData: wx.getStorageSync('userData') || {}
    })
    console.log(this.data.userData)
    wx.request({
      url: 'https://www.shananchuanmei.com/shanbay/task/get_checks/' + wx.getStorageSync('open_id'),
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        console.log('get_checks', res.data)
        if (res.data.status) {
          that.setData({
            amount: res.data.amount,
            checks: res.data.data
          })
        }
      },
    })

    if (this.data.userData.enLevel == 0 || this.data.userData == {}) {
      wx.navigateTo({
        url: '../welcome/welcome?index=0'
      })
    } else {
      wx.request({
        url: 'https://www.shananchuanmei.com/shanbay/task/set_daily/' + wx.getStorageSync('open_id'),
        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function (res) {
          // success
          console.log('set_daily:', res.data)
          if (res.data.status || !res.data.finish) {
            app.getTasks(that)
          } 
          if (res.data.finish) {
            wx.setStorageSync('finish', true)
            that.setData({
              finish: true,
              rest: 0
            })
          }
        },
      })
    }
  },
  //点击开始学习
  startStudy: function () {
    console.log('navigateTo word')
    wx.navigateTo({
      url: '../word/word'
    })
  },
  //页面显示
  onShow: function () {
    this.setData({
      userData: wx.getStorageSync('userData'),
      rest: wx.getStorageSync('rest'),
      tasks: wx.getStorageSync('tasks')
    })
  }
})
