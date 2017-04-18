//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    index: 0,
    finish: false
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
    this.setData({
      tasks: wx.getStorageSync('tasks')
    })
    for (var i in this.data.tasks) {
      console.log(i)
      if (this.data.tasks[i].status == 1) {
        this.setData({
          index: i
        })
        break
      }
    }
    this.getWord(this.data.index)
    this.getNote(this.data.index)
  },
  getWord: function (index) {
    console.log(index)
    var that = this
    var tmp_word = {
      content: this.data.tasks[index].word.content,
      wid: this.data.tasks[index].word.wid
    }
    wx.request({
      url: 'https://api.shanbay.com/bdc/search/?word=' + tmp_word.content,
      data: {},
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        console.log(res.data)
        tmp_word.definition = res.data.data.definition
        tmp_word.pron = res.data.data.pronunciation
        wx.request({
          url: 'https://api.shanbay.com/bdc/example/?vocabulary_id=' + res.data.data.id,
          method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
          // header: {}, // 设置请求的 header
          success: function (res) {
            // success
            console.log(res.data)
            tmp_word.examples = []
            for (var i in res.data.data) {
              res.data.data[i].annotation = res.data.data[i].annotation.replace(/(<\/?[a-z]*>)/g, '')
              console.log('subsite', res.data.data[i].annotation.replace(/(<\/?[a-z]*>)/g, ''))
              if (i < 3) {
                tmp_word.examples.push(res.data.data[i])
              }
            }
            that.setData({
              word: tmp_word
            })
          },
        })
        // success
      },
    })
  },
  nextWord: function () {
    var that = this
    if (this.data.index == this.data.tasks.length - 1) {
      wx.request({
        url: 'https://www.shananchuanmei.com/shanbay/task/check/' + wx.getStorageSync('open_id'),
        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function (res) {
          // success
          if (res.data.status) {
            wx.showModal({
              title: '打卡成功',
              content: '你已完成今日任务',
              showCancel: false,
              success: function (res) {
                if (res.confirm) {
                  console.log('用户点击确定')
                  wx.reLaunch({
                    url: '/pages/index/index',
                  })
                } 
              }
            })
          }
        },
      })
    } else {
      wx.request({
        url: 'https://www.shananchuanmei.com/shanbay/task/tag',
        data: {
          tid: this.data.tasks[this.data.index].tid,
          tag: 2,
        },
        header: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function (res) {
          // success
          console.log(res.data)
          var tmp_tasks = wx.getStorageSync('tasks')
          tmp_tasks[that.data.index].status = 2
          var index = that.data.index
          var rest = wx.getStorageSync('rest') -1
          index++
          // console.log('index', index)
          wx.setStorageSync('tasks', tmp_tasks)
          wx.setStorageSync('rest', rest)
          that.setData({
            tasks: tmp_tasks,
            index: index
          })

          that.getWord(index)
          that.getNote(index)
        },
      })
    }
  },
  getNote: function (index) {
    var that = this
    console.log('getNotes-index', index)
    wx.request({
      //获取所有笔记，考虑到刚开始的笔记很少，为了展示效果，所以显示所有笔记
      url: 'https://www.shananchuanmei.com/shanbay/note/get',
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        console.log('getNotes-success', res.data)
        that.setData({
          notes: res.data.data
        })
      },
    })
  },
  writeNote: function () {
    wx.navigateTo({
      url: '../writeNote/writeNote?wid=' + this.data.word.wid,
    })
  }
})
