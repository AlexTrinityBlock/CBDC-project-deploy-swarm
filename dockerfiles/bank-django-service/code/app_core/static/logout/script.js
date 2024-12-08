fetch("/api/logout", {
    // 方法為Post
    method: "POST",
    // Header 一定要加入，否則在Laravel一類的框架可能會接收不到
    headers: {
        'Content-Type': 'application/json',
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    },
    // 將要傳送的內容轉換成JSON格式
    // body: data,
}).then((response) => {
    // 將收到的回應轉換成JSON物件
    return response.json();
}).then((jsonObj) => {
    window.location.replace("/");
});