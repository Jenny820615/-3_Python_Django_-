document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', function () {
        const id = this.getAttribute('data-id'); // 獲取點擊按鈕的相對應資料的id
        const row = this.parentElement.parentElement; // 獲取相對資料的tr標籤(父元素)
        const editForm = row.nextElementSibling; // 獲取相對資料的編輯資料(兄弟元素)
        const fields = row.querySelectorAll('td'); // 找到所有td元素

        // 把原內容帶入編輯表格中當作預設值
        editForm.querySelector('input[name="new_ordername"]').value = fields[2].textContent;
        editForm.querySelector('input[name="new_receivername"]').value = fields[3].textContent;
        editForm.querySelector('input[name="new_addr"]').value = fields[4].textContent;
        editForm.querySelector('input[name="new_tel"]').value = fields[5].textContent;

        // 找到編輯表單中的id帶入表單中
        const idInput = editForm.querySelector('input[name="id"]');
        if (idInput) {
            idInput.value = id;
        }

        // 編輯表單的樣式
        editForm.style.display = 'table-row';
    });
});

// 幫編輯表單都設定監聽器
document.querySelectorAll('.edit-form').forEach(form => {
    form.addEventListener('submit', function (e) { // 提交表單時執行
        e.preventDefault(); // 阻止表單默認提交，使用js提交

        const id = this.querySelector('input[name="id"]').value; // 獲取表單中的id，設為要編輯的資料的idea
        const formData = new FormData(this); // 建立一個fromdata物件，用在把表單數據封裝成可以提交的數據

        fetch(`/edit/${id}`, {
            method: 'POST',
            body: formData
        }) // 使用Fetch API發送POST請求，以更新數據，${id}是要編輯的數據的ID

        .then(response => response.json()) // 將返回的資料解析成JSON格式
        .then(data => {
            if (data.success) {
              // 更新成功后，重新載入頁面
              location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
