### 1.pytest 执行方式

#### 第一次失败后停止
`pytest -x`
#### 第二次失败后停止
`pytest --maxfail=2`
#### 在模块中运行测试
`pytest test_xxx.py`
#### 在目录中运行测试
`pytest testing/`
#### 按关键字表达式运行测试
`pytest -k "keyword"`
#### 在模块内运行特定测试
`pytest test_xxx.py::test_xxx`
#### 指定测试方法的另一个示例
`pytest test_mod.py::TestClass::test_method`
#### 通过标记表达式运行测试
`pytest -m slow`
#### 从包运行测试
`pytest --pyargs pkg.testing`

### 2.pytest python 回溯打印
#### 在回溯中显示局部变量
`pytest --showlocals`
#### 显示局部变量（快捷方式）
`pytest -l`
#### （默认值）第一个和最后一个的“长”追溯条目，但其他条目为“短”样式
`pytest --tb=auto`
#### 详尽的，信息丰富的回溯格式
`pytest --tb=long`
#### 较短的回溯格式
`pytest --tb=short`
#### 每次故障仅一条线
`pytest --tb=line`
#### Python标准库格式
`pytest --tb=native`
#### 完全没有回溯
`pytest --tb=no`

### 3.详细测试报告
#####这个 -r 选项接受其后面的字符数
#### 失败
`f`
#### 误差
`E`
#### 跳过
`s`
#### 失败
`x`
#### XPASS
`X`
#### 通过
`p`
#### 通过输出
`P`
#### 所有(pP除外)
`a`
#### 所有 
`A`
#### 无，这不能用来显示任何内容（因为 fE 是默认设置）
`N`

### 4.下降到 PDB （python debugger）失败时
`pytest --pdb`
##### 第一次失败后下降到PDB，然后结束测试会话
`pytest -x --pdb`
##### 在前三个故障时下降到PDB
`pytest --pdb --maxfail=3`

### 5.下降到 PDB （python调试器）在测试开始时
`pytest --trace`

### 6.分析测试执行持续时间
#### 要获取长度超过1.0秒的最慢10个测试持续时间的列表：
`pytest --durations=10 --durations-min=1.0`


### 7.创建JUnitXML格式文件
#### 创建可被读取的结果文件 Jenkins 或其他持续集成服务器，使用此调用：
`pytest --junitxml=path`
#### 要设置根测试套件XML项的名称，可以配置 junit_suite_name 配置文件中的选项：
`[pytest]`

`junit_suite_name = my_suite`
#### JUnit XML规范似乎表明 "time" 属性应该报告总的测试执行时间，包括安装和拆卸 (1 ， 2 ）它是默认的pytest行为。要只报告调用持续时间，请配置 junit_duration_report 这样的选择：
`[pytest]`

`junit_duration_report = call`

#### 如果要记录测试的其他信息，可以使用 record_property 固定装置：
```python
def test_function(record_property):
    record_property("example_key", 1)
    assert True
```
```xml
<testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
  <properties>
    <property name="example_key" value="1" />
  </properties>
</testcase>
```
#### 或者，您可以将此功能与自定义标记集成：
```python
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))
```
#### 在你的测试中
```python
# content of test_function.py
import pytest


@pytest.mark.test_id(1501)
def test_function():
    assert True
```
#### 将导致
```xml
<testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
  <properties>
    <property name="test_id" value="1501" />
  </properties>
</testcase>
```
#### 要向testcase元素添加额外的xml属性，可以使用 record_xml_attribute 固定装置。这也可用于覆盖现有值：
```python
def test_function(record_xml_attribute):
    record_xml_attribute("assertions", "REQ-1234")
    record_xml_attribute("classname", "custom_classname")
    print("hello world")
    assert True
```
### 不像 record_property ，这不会添加新的子元素。相反，这将添加一个属性 assertions="REQ-1234" 在生成的 testcase 标记并重写默认值 classname 具有 "classname=custom_classname" ：
```xml
<testcase classname="custom_classname" file="test_function.py" line="0" name="test_function" time="0.003" assertions="REQ-1234">
    <system-out>
        hello world
    </system-out>
</testcase>
```
### record_xml_attribute 是一个实验性的特性，它的接口在未来的版本中可能会被更强大和通用的东西所取代。然而，功能本身将保持不变。
### 使用此 record_xml_property 在使用CI工具分析XML报告时可以提供帮助。但是，一些解析器对允许的元素和属性非常严格。许多工具使用XSD模式（如下面的示例）来验证传入的XML。确保您使用的是解析器允许的属性名。
### 下面是Jenkins用于验证XML报告的方案：
```xml
<xs:element name="testcase">
    <xs:complexType>
        <xs:sequence>
            <xs:element ref="skipped" minOccurs="0" maxOccurs="1"/>
            <xs:element ref="error" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element ref="failure" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element ref="system-out" minOccurs="0" maxOccurs="unbounded"/>
            <xs:element ref="system-err" minOccurs="0" maxOccurs="unbounded"/>
        </xs:sequence>
        <xs:attribute name="name" type="xs:string" use="required"/>
        <xs:attribute name="assertions" type="xs:string" use="optional"/>
        <xs:attribute name="time" type="xs:string" use="optional"/>
        <xs:attribute name="classname" type="xs:string" use="optional"/>
        <xs:attribute name="status" type="xs:string" use="optional"/>
    </xs:complexType>
</xs:element>
```
#### 如果要在测试套件级别添加属性节点，该节点可能包含与所有测试相关的属性，则可以使用 record_testsuite_property 会话范围的夹具：
#### 这个 record_testsuite_property 会话范围的fixture可用于添加与所有测试相关的属性。
```python
import pytest


@pytest.fixture(scope="session", autouse=True)
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property("ARCH", "PPC")
    record_testsuite_property("STORAGE_TYPE", "CEPH")


class TestMe:
    def test_foo(self):
        assert True
```
#### 夹具是一个可调用的 name 和 value A的 <property> 在生成的XML的测试套件级别添加的标记：
```xml
<testsuite errors="0" failures="0" name="pytest" skipped="0" tests="1" time="0.006">
  <properties>
    <property name="ARCH" value="PPC"/>
    <property name="STORAGE_TYPE" value="CEPH"/>
  </properties>
  <testcase classname="test_me.TestMe" file="test_me.py" line="16" name="test_foo" time="0.000243663787842"/>
</testsuite>
```
### 8.创建结果日志格式文件
#### 要创建纯文本机器可读的结果文件，可以发出：
`pytest --resultlog=path`
### 9.向在线Pastebin服务发送测试报告
`pytest --pastebin=failed`
#### 为整个测试会话日志创建URL ：
`pytest --pastebin=all`

### 9.早期加载插件
`pytest -p mypluginmodule`
#### 插件的入口点名称。这是传递给 setuptools when the plugin is registered. For example to early-load the pytest-cov 您可以使用的插件：
`pytest -p pytest_cov`

### 10.禁用插件
#### 要在调用时禁用加载特定插件，请使用 -p 选项和前缀 no: .
`pytest -p no:doctest`
