
async function RedeemVoucher(voucher_token,) {
    /**
     * 領錢
     * @param {string} voucher_token - 點數卡的 Token
     */
    let data = {
        "voucher_token": voucher_token,
    }

    let result = await fetch('/api/redeem/voucher', {
        // 方法為Post
        method: "POST",
        // Header 一定要加入，否則在Laravel一類的框架可能會接收不到
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        // 將要傳送的內容轉換成JSON格式
        body: new URLSearchParams(data),
    }).then((response) => {
        // 將收到的回應轉換成JSON物件
        return response.json();
    }).then((jsonObj) => {
        // 若登入成功
        if (jsonObj['code'] == 1) {
            return jsonObj
        } else {
            return jsonObj
        }
    });

    return  result;
}

export default RedeemVoucher