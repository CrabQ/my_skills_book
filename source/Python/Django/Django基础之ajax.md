# Django基础之ajax

## html代码

```html
<script>
    $('#btn').click(function () {
        $.ajax({
            url: '{% url 'login' %}',
            type: 'post',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                csrfmiddlewaretoken: '{{ csrf_token }}',
                // csrfmiddlewaretoken:$('[name=csrfmiddlewaretoken]').val(),
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

## 注意点

```python
if username == '1' and password == '2':
    res = {'code':200, 'msg': reverse('books')}
else:
    res = {'code':400, 'msg': '账号密码错误'}
return JsonResponse(res)

# 返回列表
# return JsonResponse([1,2], safe=False)

# 如果使用HttpResponse, 不使用JsonResponse返回数据, 前端页面要解析成json格式
# return HttpResponse({'code':200, 'msg': reverse('books')})
# var resStr = JSON.parse(res);
```

## Django获取上传文件

### 通过form表单上传

```python
# <form action="" method="post" enctype="multipart/form-data">
#   {% csrf_token %}
#   头像: <input type="file" name="head_pic">
#   <input type="submit">
# </form>

def login(request):
        head_pic = request.FILES.get('head_pic')
        with open(head_pic.name, 'wb') as f:
            for i in head_pic:
                f.write(i)
            # for chunk in head_pic.chunks():
            #     f.write(chunk)
```

### 通过ajax上传, views函数不变,前端页面修改

```html
<script>
    $('#btn').click(function () {
        var formdata = new FormData();
        formdata.append(username,$('#username').val());
        formdata.append(password,$('#password').val());
        formdata.append('csrfmiddlewaretoken','{{ csrf_token }}');
        formdata.append('head_pic',$('#file')[0].files[0]);
        $.ajax({
            url: '{% url 'login' %}',
            type: 'post',
            data: formdata,
            processData: false,    // 不处理数据
            contentType: false,
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
