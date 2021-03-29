#### 1.approx 断言两个数字（或两组数字）在某些公差内彼此相等。
```python
from pytest import approx

print(approx(0.1 + 0.2 == approx(0.3)))
```

### 2.fail 
```python
import pytest

@pytest.fail(msg='测试失败')
def test_the_fail():
    pass

```


#### 
```python
import pytest

@pytest.mark.skip(reason='当前无法测试')
def test_the_unknown():
    raise NameError
```