# ajax基础

```html
<!-- 如果在form表单中,form表单的type要修改为button,不然form表单的提交按钮会触发form表单的action -->
<!-- input type="button" -->
<script>
    $('#btn').click(function () {
        $.ajax({
            url: '/home',
            type: 'post',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
            },
            success: function (res) {
                console.log(res);
                if (res.code === 200) {
                    location.href = res.msg
                } else {
                    $('#error').text(res.msg)
                }
            },
        })
    })
</script>
```
