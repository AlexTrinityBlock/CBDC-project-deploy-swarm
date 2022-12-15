import CheckLoginStatus from '/static/login/CheckLoginStatus.js'

// 主函數
async function main() {
    // // 驗證登入成功與否
    // let result = await CheckLoginStatus(token)
    // // 假如沒有登入成功則跳轉回登入頁面
    // if (! result) {
    //     window.location.replace("/login");
    // }
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}