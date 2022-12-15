import AddVoucher from "/static/administrator_issue_voucher/AddVoucher.js"
import GetVoucherList from "/static/administrator_issue_voucher/GetVoucherList.js"

// 舊點數卡資料
var oldVoucherList = ''

// 新增點數卡增加按鈕觸發
function add_voucher_button_handler() {
    add_voucher_btn.onclick = async () => {
        let addVoucherResult = await AddVoucher(amount_input.value)
        if (addVoucherResult.code == 1){
            Swal.fire({
                icon: 'success',
                title: 'Success !',
            })
            amount_input.value = 0
        }
    }
}

// 渲染點數卡畫面
function rend_voucher_list(vouchersObj){
    vouchersObj.forEach((element) => {
        // 錢幣是否被使用
        let isUsed = ''
        if(element.is_used == 1){
            isUsed = `<p style="color:red">此錢幣已經被使用</p>`
        }else{
            isUsed = `<p style="color:green">此錢幣尚未被使用</p>`
        }

        let labelColor = ''
        if(element.is_used == 1){
            labelColor = `style="color:red"`
        }else{
            labelColor = `style="color:green"`
        }

        let text = `
        <div class='accordion-item'>
            <h2 class='accordion-header' id='obj-`+element.voucher_token+`'>
                <button class='accordion-button collapsed' type='button' data-bs-toggle='collapse'`+labelColor+`
                    data-bs-target='#flush-collapse`+element.voucher_token+`' aria-expanded='false'
                    aria-controls='flush-collapseOne'>
                    `+element.voucher_token+`
                </button>
            </h2>
            <div id='flush-collapse`+element.voucher_token+`' class='accordion-collapse collapse'
                aria-labelledby='obj-`+element.voucher_token+`' data-bs-parent='#accordionFlush'>
                <div class='accordion-body' `+labelColor+`>
                    點數 token: `+element.voucher_token+`<br>
                    `+isUsed+`<br>
                    額度: `+element.currency+`
                    <div id='qr`+element.voucher_token+`' ></div>
                </div>
            </div>
        </div>
        `;
        accordionFlush.innerHTML = accordionFlush.innerHTML+text
    });
}

// 繪製QRCode
function qrcode(vouchersObj){
    vouchersObj.forEach((element) => {
        if (element.is_used == 1){return}
        let qrcode = new QRCode(document.getElementById("qr"+element.voucher_token), {
            colorDark : "green",
        });	
        qrcode.clear();
        qrcode.makeCode(element.voucher_token);
    })
}

// 更新點數卡
async function update_voucher_list() {
    let listVoucherResult = await GetVoucherList()
    listVoucherResult = listVoucherResult.vouchers
    let vouchersObj = JSON.parse(listVoucherResult)
    rend_voucher_list(vouchersObj)
    qrcode(vouchersObj)

    window.setInterval(async () => {
        let listVoucherResult = await GetVoucherList()
        listVoucherResult = listVoucherResult.vouchers
        // 假如數值沒有更新則結束
        if (oldVoucherList == listVoucherResult) { return }
        // 更新數值
        oldVoucherList = listVoucherResult
        let vouchersObj = JSON.parse(listVoucherResult)
        // 清理舊資料
        accordionFlush.innerHTML = ''
        rend_voucher_list(vouchersObj)
        qrcode(vouchersObj)
    }, 1000);
}

// 主函數
function main() {
    add_voucher_button_handler()
    update_voucher_list()
}

// 當頁面完全載入後啟動主函數
window.onload = function () {
    main()
}