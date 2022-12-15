async function GetUserAccount(){
    let result = await  fetch("/api/get/account?" + new URLSearchParams({
    }),
        {
            // Get方法
            method: "get",
            // Header 一定要加入，否則在Laravel一類的框架可能會接收不到
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            }
        }).then((response) => {
            // 將收到的回應轉換成JSON物件
            return response.json();
        }).then((jsonObj) => {
            // 若登入成功
            if (jsonObj['code'] == 1){
                return jsonObj['account']
            }else{
                return false
            }
        });

    return result
}

export default GetUserAccount