//writeNote.js
Page({
    onLoad: function (options) {
        console.log(options)
        this.setData({
            wid: options.wid
        })
    },
    submit: function (e) {
        var content = e.detail.value.textarea
        wx.showLoading({
      title: '提交中',
    })
    setTimeout(function () {
      wx.hideLoading()
    }, 6000)
        wx.request({
            url: 'https://www.shananchuanmei.com/shanbay/note/create',
            data: {
                openId: wx.getStorageSync('open_id'),
                content: content,
                wid: this.data.wid
            },
            header: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            // header: {}, // 设置请求的 header
            success: function (res) {
                // success
                console.log('success-writeNote', res.data)
                if (res.data.status) {
                    wx.redirectTo({
                        url: '../word/word',
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
})