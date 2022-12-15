import GetTransactionLog from "/static/administrator_transaction_log/GetTransactionLog.js"

// 舊點數卡資料
var oldTransactionLogList = ''

// 渲染交易紀錄畫面
function rend_transactionLog_list(transactionLogsObj){
    transactionLogsObj.forEach((element) => {
        console.log(element)
        let labelColor = ''
        let status = ''
        if(element.status == 0){
            labelColor = `style="color:red"`
            status = '失敗'
        }else{
            labelColor = `style="color:green"`
            status = '成功'
        }

        let text = `
        <div class='accordion-item'>
            <h2 class='accordion-header' id='obj-`+element.id+`'>
                <button class='accordion-button collapsed' type='button' data-bs-toggle='collapse'`+labelColor+`
                    data-bs-target='#flush-collapse`+element.id+`' aria-expanded='false'
                    aria-controls='flush-collapseOne'>
                    `+element.log_time+`
                </button>
            </h2>
            <div id='flush-collapse`+element.id+`' class='accordion-collapse collapse'
                aria-labelledby='obj-`+element.id+`' data-bs-parent='#accordionFlush'>
                <div class='accordion-body' `+labelColor+`>
                    使用者ID: `+element.user_id+`<br>
                    交易型態: `+element.type+`<br>
                    狀態: `+status+`<br>
                    系統訊息: `+element.message+`<br>
                    金額: `+element.amount+`<br>
                    貨幣內容: <br>
                    <div class="used_currency">
                        <code >
                            `+ element.used_currency;+`
                        </code>
                    </div>
                    <div id='qr`+element.id+`' ></div>
                </div>
            </div>
        </div>
        `;
        accordionFlush.innerHTML = accordionFlush.innerHTML+text
    });
}

// 更新點數卡
async function update_transactionLog_list() {
    let listTransactionLogResult = await GetTransactionLog()
    let transactionLogsObj = JSON.parse(listTransactionLogResult.transaction_logs)
    rend_transactionLog_list(transactionLogsObj)
    oldTransactionLogList = listTransactionLogResult.transaction_logs

    window.setInterval(async () => {
        let listTransactionLogResult = await GetTransactionLog()
        listTransactionLogResult = listTransactionLogResult.transaction_logs
        // 假如數值沒有更新則結束
        if (oldTransactionLogList == listTransactionLogResult) { return }
        // 更新數值
        oldTransactionLogList = listTransactionLogResult
        let transactionLogsObj = JSON.parse(listTransactionLogResult)
        // 清理舊資料
        accordionFlush.innerHTML = ''
        rend_transactionLog_list(transactionLogsObj)

    }, 1000);
}

// 主函數
function main() {
    update_transactionLog_list()
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}