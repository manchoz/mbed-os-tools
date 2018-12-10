import os
from builtins import super

from . import MockTestEnvironment

class MockTestEnvironmentWindows(MockTestEnvironment):

    def __init__(self, test_case, platform_info, image_path):
        super().__init__(test_case, platform_info, image_path)

        self.patch('os.name', new='nt')

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)

        if value:
            return False

        # Assert for proper image copy
        mocked_call = self.patches[
            'mbed_os_tools.test.host_tests_plugins.host_test_plugins.call'
        ]

        first_call_args = mocked_call.call_args_list[0][0][0]
        self._test_case.assertEqual(first_call_args[0], "copy")
        self._test_case.assertEqual(first_call_args[1], self._image_path)
        self._test_case.assertTrue(first_call_args[2].startswith(self._platform_info["mount_point"]))
        self._test_case.assertTrue(first_call_args[2].endswith(os.path.splitext(self._image_path)[1]))

        # Ensure only one subprocess was started
        self._test_case.assertEqual(len(mocked_call.call_args_list), 1)
