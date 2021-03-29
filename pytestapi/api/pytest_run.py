from pytestapi.api import router
from pytestapi.command import Command
from pytestapi.forms.args import PytestArg
from pytestapi.view_models.result import TestResult


@router.post("/pytest/run", tags=["pytest 执行测试"])
async def run(arg: PytestArg):
    output = Command('pytest', arg=arg).output
    return TestResult(output).to_dict()


@router.post("/pytest/run/scope", tags=["按节点id、在目录、模块中运行测试"])
async def run_tests_by_node_ids(arg: PytestArg):
    """
    1.按节点id运行测试 eg. test_mod.py::TestClass::test_method
    2.在模块中运行测试 eg. test_mod.py
    3.在目录中运行测试 eg. testing/
    :param arg:
    :return:
    """
    output = Command('pytest', arg=arg).output
    return TestResult(output).to_dict()


@router.get("/pytest/fixtures", tags=["获取pytest fixtures"])
async def get_pytest_fixtures():
    arg = PytestArg()
    arg.r_arg = '--fixtures'
    output = Command('pytest', arg=arg).output
    return output


@router.post("/pytest/maxfail", tags=["允许测试失败最大次数"])
async def stop_after_failures(arg: PytestArg):
    arg.r_arg = f'--maxfail={arg.r_arg}'
    output = Command('pytest', arg=arg).output
    return TestResult(output).to_dict()


@router.post("/pytest/run/keyword", tags=["根据关键字表达式运行测试"])
async def run_tests_by_keyword(arg: PytestArg):
    arg.r_arg = '"'+arg.r_arg+'"'
    output = Command('pytest -k', arg=arg).output
    return TestResult(output).to_dict()


@router.post("/pytest/run/marker", tags=["通过标记表达式运行测试"])
async def run_tests_by_marker(arg: PytestArg):
    output = Command('pytest -m', arg=arg).output
    return TestResult(output).to_dict()


@router.post("/pytest/run/packages", tags=["从包运行测试"])
async def run_tests_from_packages(arg: PytestArg):
    output = Command('pytest --pyargs', arg=arg).output
    return TestResult(output).to_dict()


@router.post("/pytest/list")
async def get_slowest_list(arg: PytestArg):
    arg.r_arg = f'--durations={arg.r_arg}'
    arg.p_arg = f'--durations-min={arg.p_arg}'
    output = Command('pytest', arg=arg).output
    return TestResult(output).to_dict()
