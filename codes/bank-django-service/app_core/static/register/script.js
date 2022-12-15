// 送出函數
function sendMessage() {
    // Fetch函數
    const data = JSON.stringify({
        'account': account.value,
        'password': password.value,
        'e_mail': e_mail.value,
        'user_name':user_name.value,
        'home_address':home_address.value,
        'phone': phone.value
    })


    fetch("/api/register", {
        // 方法為Post
        method: "POST",
        // Header 一定要加入，否則在Laravel一類的框架可能會接收不到
        headers: {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        },
        // 將要傳送的內容轉換成JSON格式
        body: data,
    }).then((response) => {
        // 將收到的回應轉換成JSON物件
        return response.json();
    }).then(async (jsonObj) => {
        // 若登入成功
        if (jsonObj['code'] == 1) {
            LoginFail.innerHTML = "註冊成功"
            await new Promise(r => setTimeout(r, 1000));
            window.location.replace("/login");
        } else if(jsonObj['code'] == 2){
            LoginFail.innerHTML = "帳號已經被註冊"
        } else if(jsonObj['code'] == 0){
            LoginFail.innerHTML = "請確認每個欄位都有輸入"
        }
    });
}

//處理密碼不吻合
function handlePasswordMatch(){
    if ( password.value != password_check.value){
        LoginFail.innerHTML = "兩次密碼不吻合"
        return false
    }
    return true
}

// 檢查Email是否符合格式
function handleValidateEmail() 
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(e_mail.value))
  {
    return (true)
  }
  LoginFail.innerHTML = "E-mail 格式不符合"
    return (false)
}

//

// 將註冊送出
function submit() {
    if (!handleValidateEmail()){return} // Email格式不符合就結束
    if (!handlePasswordMatch()){return} //如果兩次密碼不吻合則結束
    sendMessage()
}

// 主函數
async function main() {
    // 將註冊按鈕綁定註冊函數
    document.getElementById("submit").onclick = submit;
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}