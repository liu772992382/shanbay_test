//【个人界面】 pages/untitled(1)/untitled(1).js
var app = getApp()
Page({
  data: {
    bookArray: ['4级词汇', '6级词汇', '雅思词汇', '托福词汇'],
    taskArray: [5, 15, 25, 50, 100],
    index: 0,
    userInfo: {},
  },
  onShow: function () {
    var that = this
    this.setData({
      userData: wx.getStorageSync('userData')
    })
  },
  bindPickerChange: function (e) {
    var that = this
    console.log('pickerChange', e.detail.value)
    if (wx.getStorageSync('finish')) {
      wx.showModal({
        title: '提示',
        content: '你已完成今日任务，不能修改每日任务',
        showCancel: false,
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击确定')
          }
        }
      })
    } else {
      var tmp_task = this.data.taskArray[e.detail.value]
      this.setData({
        index: e.detail.value
      })
      wx.request({
        url: 'https://www.shananchuanmei.com/shanbay/user/update',
        header: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: {
          openId: wx.getStorageSync('open_id'),
          task: tmp_task
        },
        method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function (res) {
          // success
          console.log('set-task', res.data)
          if (res.data.status) {
            var tmp_user = wx.getStorageSync('userData')
            tmp_user.task = tmp_task
            wx.setStorageSync('userData', tmp_user)
            app.getTasks()
            that.setData({
              userData: tmp_user
            })
          }
        },
      })
    }

  },
  chooseBook: function () {
    wx.navigateTo({
      url: '../welcome/welcome?index=1'
    })
  }
})
