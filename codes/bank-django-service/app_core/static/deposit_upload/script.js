import GetBalance from "/static/deposit_upload/GetBalance.js"
import RedeemCurrency from "/static/deposit_upload/RedeemCurrency.js"
import GetPaymentID from "/static/deposit_upload/GetPaymentID.js"

var oldQRcode = ''
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
                title: '+ $' + (balance - oldBalance),
            })
        }

        oldBalance = balance;
    }, 1000);
}

// 處理上傳檔案
function file_handler() {
    currency_file.addEventListener('change', async (event) => {
        // 讀取檔案
        let file = await event.target.files[0];
        let filexText = await file.text();
        let currency = JSON.parse(filexText);
        // 寫入變數
        let Info = currency.Info
        let message = currency.message
        let t = currency.t
        let s = currency.s
        let R = currency.R
        // 取得支付ID
        let payment_id = await GetPaymentID()
        // 開啟等待圓球
        upload_spinner.style.display = "block";
        // 關閉上傳按鈕
        currency_file.style.display = "none";
        // 傳送給銀行
        let result = await RedeemCurrency(payment_id, message, Info, R, s, t)
        // 關閉等待圓球
        upload_spinner.style.display = "none";
        // 開啟上傳按鈕
        currency_file.style.display = "block";
        // 清除上傳內容
        currency_file.value = null

        if (result.code == 1) {
            // Swal.fire({
            //     icon: 'success',
            //     title: '貨幣儲存成功 !',
            // })
        } else {
            Swal.fire({
                icon: 'error',
                title: '無效的貨幣!',
            })
        }
    });
}

// QR cdoe
async function qr_code() {
    await new Promise(r => setTimeout(r, 500));
    const html5QrCode = new Html5Qrcode("reader");
    const config = { fps: 10, qrbox: { width: 1000, height: 1000 } };
    html5QrCode.start({ facingMode: "environment" }, config, async (decodedText, decodedResult) => {
        // 收到一樣的訊息則退出
        if (oldQRcode == decodedText) { return }
        // 關閉攝影機
        html5QrCode.stop()
        // 解析收到的內容
        let currency = JSON.parse(decodedText);
        // 寫入變數
        let Info = currency.Info
        let message = currency.message
        let t = currency.t
        let s = currency.s
        let R = currency.R
        // 取得支付ID
        let payment_id = await GetPaymentID()
        // 傳送給銀行
        let result = await RedeemCurrency(payment_id, message, Info, R, s, t)
        oldQRcode = decodedText
        // 回傳錯誤訊息
        if (result.code == 0) {
            Swal.fire({
                icon: 'error',
                title: '無效的 QR code',
            })
        }
        // 等待 0.5 秒後重新展開攝影機
        await new Promise(r => setTimeout(r, 500));
        qr_code()
    });

}

// tab點擊事件
function tab_handler() {
    qr_code()
    nav_tab_1.onclick = async () => {
        qr_code()
    }
}

// 主函數
function main() {
    load_balance();
    file_handler();
    qr_code();
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}
