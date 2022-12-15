import GetBalance from "/static/pay_qr_code_page/GetBalance.js"
import GetPaymentID from "/static/pay_qr_code_page/GetPaymentID.js"

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

//建立 QR code
async function qr_code() {
    let payment_id = await GetPaymentID()
    let qrcode = new QRCode(document.getElementById("qr_code"), {
        colorDark: "#0066cc",
    });
    qrcode.makeCode(payment_id);
}

//顯示付款代碼
async function display_payment_id() {
    let payment_id = await GetPaymentID()
    payment_id_div.innerHTML = payment_id
}

// 主函數
function main() {
    load_balance();
    qr_code();
    display_payment_id();
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}