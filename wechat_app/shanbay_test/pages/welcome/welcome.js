//welcome.js
//获取应用实例
var app = getApp()
Page({
  data: {
    userInfo: {}
  },
  onLoad: function (options) {
    var that = this
    this.setData({
      index: options.index
    })
    console.log('welcome:load')
    wx.request({
      url: 'https://www.shananchuanmei.com/shanbay/book/get_all',
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        console.log(res.data)
        res.data.data[0]['checked'] = true
        that.setData({
          books: res.data.data
        })
      },
      fail: function (res) {
        // fail
      },
      complete: function (res) {
        // complete
      }
    })
  },
  formSubmit: function (e) {
    var that = this
    console.log('formSubmit', e)
    var book = e.detail.value.book
    wx.request({
      url: 'https://www.shananchuanmei.com/shanbay/user/update',
      data: {
        openId: wx.getStorageSync('open_id'),
        enLevel: book
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        console.log(res.data)
        if (res.data.status) {
          var tmp_data = wx.getStorageSync('userData')
          tmp_data.enLevel = book
          wx.setStorageSync('userData', tmp_data)
          wx.request({
            url: 'https://www.shananchuanmei.com/shanbay/task/create/' + wx.getStorageSync('open_id'),
            method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            // header: {}, // 设置请求的 header
            success: function (res) {
              // success
              console.log(res.data)
              if (res.data.status) {
                wx.reLaunch({
                  url: that.data.index==0 ? '/pages/index/index' : '/pages/person/person'
                })
              }
            },
            fail: function (res) {
              // fail
            },
            complete: function (res) {
              // complete
            }
          })
        }
      },
    })
  }
})
