import GetUserAccount from "/static/home2/GetUserAccount.js"
import GetBalance from "/static/home2/GetBalance.js"

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

// 載入使用者帳號
async function load_account() {    
    user_account.innerHTML = await GetUserAccount();
}

// 主函數
function main() {
    load_account();
    load_balance();
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}