
async function AddVoucher(amount) {
    /**
     * 領錢
     * @param {number} amount - 領取的額度
     */
    let data = {
        "amount": amount,
    }

    let result = await fetch('/api/generate/voucher', {
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
            console.log(jsonObj)
        }
    });
    // let json_string = JSON.stringify(result);

    return  result;
}

export default AddVoucher