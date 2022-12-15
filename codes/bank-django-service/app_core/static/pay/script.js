import GetBalance from "/static/pay/GetBalance.js"
import Withdraw from "/static/pay/Withdraw.js"
import GetToken from "/static/pay/GetToken.js"
import Pay from "/static/pay/Pay.js"

var amount = 0;
var user_payment_id = null;
var url = "/api/withdraw/test"

var oldBalance = 0;

// 載入餘額
async function load_balance() {
    // 取得貨幣
    let balance = await GetBalance();
    oldBalance = balance;
    balance_text.innerHTML = '$' + balance

    // 刷新貨幣額度
    window.setInterval(async () => {
        let balance = await GetBalance();

        balance_text.innerHTML = '$' + balance
        if (balance > oldBalance) {
            Swal.fire({
                icon: 'success',
                title: '+ $'+(balance - oldBalance),
            })
        }

        oldBalance = balance;
    }, 1000);
}

// 付款流程-1(輸入支付金額)
function payment_process_1_handler() {
    payment_amount_btn.addEventListener("click", () => {        
        amount = payment_amount_input.value
        payment_form.style.display = "none";
        payment_process_2()
    }, false);
}

// 付款流程-2(顯示攝影機)
async function payment_process_2() {
    const html5QrCode = new Html5Qrcode("reader");
    const config = { fps: 10, qrbox: { width: 1000, height: 1000 } };
    html5QrCode.start({ facingMode: "environment" }, config, (decodedText, decodedResult) => {
        user_payment_id = decodedText
        html5QrCode.stop()
        payment_process_3()
    });
}

// 付款流程-3
async function payment_process_3(){
    console.log(amount)//支付金額
    console.log(user_payment_id)//支付對象的ID
    let token = await GetToken();//取得使用者識別

    // 測試支付
    let testCurrency = await Withdraw(token, 0,url);//取得0元貨幣
    // JSON解析貨幣
    testCurrency = JSON.parse(testCurrency);
    let testInfo = testCurrency.Info
    let testMessage = testCurrency.message
    let testT = testCurrency.t
    let testS = testCurrency.s
    let testR = testCurrency.R
    let testResult =await Pay(user_payment_id,testMessage,testInfo,testR,testS,testT)
    if(testResult.code!=1){
        payment_form.style.display = "block";
        Swal.fire({
            icon: 'error',
            title: '轉帳失敗!',
            text: '轉帳失敗，但金額不會缺失，請確認掃描的QR code 是否正確。',
        })
        return;
    }

    // 實際支付
    let currency = await Withdraw(token, amount,url);//取得貨幣
    // JSON解析貨幣
    currency = JSON.parse(currency);
    let Info = currency.Info
    let message = currency.message
    let t = currency.t
    let s = currency.s
    let R = currency.R
    let result =await Pay(user_payment_id,message,Info,R,s,t)
    payment_form.style.display = "block";
    payment_amount_input.value = 0

    if(result.code == 1){
        Swal.fire({
            icon: 'success',
            title: '支付成功 !',
        })
    }
}

// 主函數
function main() {
    load_balance();
    payment_process_1_handler();
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}