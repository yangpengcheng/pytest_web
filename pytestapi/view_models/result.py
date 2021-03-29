import re
from functools import lru_cache


class TestResult:
    _test_session_starts = 'test session starts'
    _failures = 'FAILURES'
    _warnings_summary = 'warnings summary'
    _short_test_summary_info = 'short test summary info'
    _test_answer = "test_answer"
    _slowest_durations = "slowest"

    def __init__(self, result):
        self.data = result
        self.time = self._parse_time()
        self.failed = self._parse("failed")
        self.passed = self._parse("passed")
        self.skipped = self._parse("skipped")
        self.xfailed = self._parse("xfailed")
        self.xpassed = self._parse("xpassed")
        self.error = self._parse("error")
        self.warnings = self._parse("warnings")
        self.deselected = self._parse("deselected")
        self.slowest_durations = self.get_slowest_durations()
        self.short_test_summary_info = self.get_short_test_summary_info()
        self.warnings_summary = self.get_warnings_summary()
        self.test_answer = self.get_test_answer()
        self.env_info = self._get_env_info()
        self.root_dir = self._get_root_dir()
        self.collected_items = self._get_collected_items()

    def _get_env_info(self):
        index = self.get_index_by_text(self._test_session_starts)
        if index or index == 0:
            return self.data[index + 1: index + 2][0]

    def _get_root_dir(self):
        index = self.get_index_by_text(self._test_session_starts)
        if index or index == 0:
            return self.data[index + 2: index + 3][0]

    def _get_collected_items(self):
        index = self.get_index_by_text(self._test_session_starts)
        if index or index == 0:
            # return re.search(r'collected\s(?P<items>\d)\sitem', self.data[index + 3: index + 4][0]
            #                  ).groupdict().get('items')
            return self.data[index + 3: index + 4][0]

    def _parse_time(self):
        return re.search(r'in\s(?P<time>.*s)', self.data[-1]).groupdict().get('time')

    def _parse(self, field):
        print(field)
        pattern = r'((?P<' + field + r'>\d)\s' + field + ')'

        if re.search(pattern, self.data[-1]):
            return re.search(pattern, self.data[-1]).groupdict().get(field)

    @lru_cache(maxsize=10)
    def get_index_by_text(self, text):
        for index, t in enumerate(self.data):
            if re.search(text.replace('\\', ''), t):
                return index

    def get_short_test_summary_info(self):
        index = self.get_index_by_text(self._short_test_summary_info)

        return "\n".join(self.data[index:-1])

    def get_warnings_summary(self):
        warnings_index = self.get_index_by_text(self._warnings_summary)
        short_index = self.get_index_by_text(self._short_test_summary_info)

        if warnings_index and short_index:
            return "\n".join(self.data[warnings_index: short_index])

    def get_slowest_durations(self):
        slowest_index = self.get_index_by_text(self._slowest_durations)
        short_index = self.get_index_by_text(self._short_test_summary_info)

        if slowest_index and short_index:
            return "\n".join(self.data[slowest_index: short_index])

        print(slowest_index, short_index)

    def get_test_answer(self):
        answer_index = self.get_index_by_text(self._test_answer)
        warnings_index = self.get_index_by_text(self._warnings_summary)

        if answer_index and warnings_index:
            return "\n".join(self.data[answer_index: warnings_index])

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key != 'data'}
