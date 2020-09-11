# subprocess

```python
import subprocess

obj = subprocess.Popen('dir .', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(obj)
res = obj.stdout.read()
print(res.decode('GBK'))

err = obj.stderr.read()
print(err.decode('GBK'))
```
