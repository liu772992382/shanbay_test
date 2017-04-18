//app.js
App({
  globalData: {
    appid: 'wxb760f4d49be6cab6',
    secret: 'fbc88be10217325ae234541147826014',
    userData: {}
  },
  onLaunch: function () {
    var that = this
    console.log('onLaunch')
    var open_id = wx.getStorageSync('open_id') || ''
    var expires_in = wx.getStorageSync('expires_in')
    var userInfo = wx.getStorageSync('userInfo') || {}
    if ((!open_id || (expires_in || Date.now()) > (Date.now() + 3600000))) {
      wx.login({
        success: function (res) {
          // console.log('login', res)
          if (res.code) {
            var js_code = res.code
            wx.getUserInfo({
              success: function (res) {
                var objz = {};
                objz.avatarUrl = res.userInfo.avatarUrl;
                objz.nickName = res.userInfo.nickName;
                objz.city = res.userInfo.city;
                objz.gender = res.userInfo.gender;
                //console.log(objz);  
                // console.log('userInfo:', objz)
                wx.setStorageSync('userInfo', objz);//存储userInfo  
                var d = that.globalData;//这里存储了appid、secret、token串   
                // console.log(d)
                var l = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + d.appid + '&secret=' + d.secret + '&js_code=' + js_code + '&grant_type=authorization_code';
                wx.request({
                  url: l,
                  data: {},
                  method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT    
                  // header: {}, // 设置请求的 header    
                  success: function (res) {
                    var obj = {};
                    obj.openid = res.data.openid;
                    obj.expires_in = Date.now() + res.data.expires_in;
                    // console.log(obj);
                    wx.setStorageSync('open_id', obj.openid);
                    //存储openid                  
                    wx.setStorageSync('expires_in', obj.expires_in)

                    that.setLogin()
                  }
                })
              }, fail: function () {
                console.log('login_fail', res)
              }
            });
          } else {
            console.log('获取用户登录态失败！' + res.errMsg)
          }
        }
      });
    } else {
      // console.log('else')
    }
  },

  setLogin: function () {
    var that = this
    wx.request({
      url: 'https://www.shananchuanmei.com/shanbay/user/login',
      data: {
        openId: wx.getStorageSync('open_id') || '',
        city: wx.getStorageSync('userInfo').city || '',
        gender: wx.getStorageSync('userInfo').gender || '',
        nickName: wx.getStorageSync('userInfo').nickName || '',
        avatarUrl: wx.getStorageSync('userInfo').avatarUrl || ''
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        if (res.data.status) {
          // console.log(res.data)
          wx.setStorageSync('userData', res.data.data)
          console.log('success login')
        } else {
          console.log('failed login')
        }
      },
      fail: function (res) {
        // fail
      },
      complete: function (res) {
        // complete
        wx.reLaunch({
          url: '/pages/index/index'
        })
      }
    })
  },
  getUserInfo: function (cb) {
    var that = this
    if (this.globalData.userInfo) {
      typeof cb == "function" && cb(this.globalData.userInfo)
    } else {
      //调用登录接口
      wx.login({
        success: function () {
          wx.getUserInfo({
            success: function (res) {
              that.globalData.userInfo = res.userInfo
              typeof cb == "function" && cb(that.globalData.userInfo)
            }
          })
        }
      })
    }
  },
  getTasks: function (that) {
    wx.request({
      url: 'https://www.shananchuanmei.com/shanbay/task/get/' + wx.getStorageSync('open_id'),
      method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      // header: {}, // 设置请求的 header
      success: function (res) {
        // success
        console.log('get_tasks', res.data)
        if (res.data.status) {
          wx.setStorageSync('tasks', res.data.data)
          wx.setStorageSync('rest', res.data.data.length)
          if(that){
          that.setData({
            tasks: res.data.data,
            rest: res.data.data.length
          })
          }
        }
      },
    })
  }
})


// App({
//   onLaunch: function () {
//     //调用API从本地缓存中获取数据
//     var logs = wx.getStorageSync('logs') || []
//     logs.unshift(Date.now())
//     wx.setStorageSync('logs', logs)
//   },

//   globalData:{
//     userInfo:null
//   }
// })




