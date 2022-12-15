
async function Pay(bank_user_payment_id,message,Info,R,s,t) {
    /**
     * 領錢
     * @param {string} bank_user_payment_id - 要被支付者的支付ID
     * @param {string} message - 使用者的秘密訊息
     * @param {string} Info - 銀行跟使用者的公開共識訊息
     * @param {string} R - 簽章
     * @param {string} s - 簽章
     * @param {string} t - 簽章
     */
    let data = {
        'bank_user_payment_id': bank_user_payment_id,
        'message': message,
        'Info':Info,
        'R':R,
        's':s,
        't':t,
    }

    let result = await fetch("/api/redeem/currency", {
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
        return jsonObj
    });
    // let json_string = JSON.stringify(result);

    return  result;
}

export default Pay