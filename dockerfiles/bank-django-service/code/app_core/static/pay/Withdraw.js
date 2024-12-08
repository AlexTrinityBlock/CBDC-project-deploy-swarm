
async function Withdraw(token,withdraw,url) {
    /**
     * 領錢
     * @param {string} token - 使用者的token
     * @param {number} withdraw - 領取的額度
     */
    let data = {
        'token': token,
        "withdraw": withdraw,
    }

    let result = await fetch(url, {
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
    let json_string = JSON.stringify(result);
    // json_string = json_string.replaceAll("\\", "");
    // console.log(json_string)
    return  json_string;
}

export default Withdraw