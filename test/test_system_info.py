
import unittest

from src.system_info import (
    get_cpu_usage,
    get_memory_info,
    get_disk_info
)


class TestSystemInfo(unittest.TestCase):

    def test_cpu_usage(self):
        cpu = get_cpu_usage()

        self.assertIsInstance(cpu, (int, float))
        self.assertGreaterEqual(cpu, 0)
        self.assertLessEqual(cpu, 100)

    def test_memory_info(self):
        memory = get_memory_info()

        self.assertIn("usage_percent", memory)

        self.assertGreaterEqual(
            memory["usage_percent"], 0
        )

        self.assertLessEqual(
            memory["usage_percent"], 100
        )

    def test_disk_info(self):
        disk = get_disk_info()

        self.assertIn("usage_percent", disk)

        self.assertGreaterEqual(
            disk["usage_percent"], 0
        )

        self.assertLessEqual(
            disk["usage_percent"], 100
        )


if __name__ == "__main__":
    unittest.main()
