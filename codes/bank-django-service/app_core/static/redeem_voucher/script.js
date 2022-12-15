import GetBalance from "/static/redeem_voucher/GetBalance.js"
import RedeemVoucher from "/static/redeem_voucher/RedeemVoucher.js"

var oldQRText = ''
var oldBalance = 0
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

// QR code scanner 
async function qr_scanner() {
    const html5QrCode = new Html5Qrcode("reader");
    const config = { fps: 10, qrbox: { width: 1000, height: 1000 } };
    html5QrCode.start({ facingMode: "environment" }, config, (decodedText, decodedResult) => {
        if(decodedText == oldQRText){return} // 若是舊的 QR code 就停止。
        html5QrCode.stop()
        oldQRText = decodedText
        process_2(decodedText)
    });
}

// 支付步驟1
async function process_1() {
    qr_scanner();
}

// 支付步驟2
async function process_2(decodedText) {
    let redeemResult = await RedeemVoucher(decodedText)
    if (redeemResult.code == 0) {
        Swal.fire({
            icon: 'error',
            title: '儲值失敗 !',
            text:'請檢查儲值條碼是否正確，或被使用。'
        })
    }
    init()
}

// 初始化支付
async function init() {
    await new Promise(r => setTimeout(r, 500));
    process_1();
}

// 主函數
function main() {
    load_balance();
    process_1();
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}