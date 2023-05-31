import unittest
from unittest.mock import patch
import os
import tempfile

from src.typedenv.main import GetEnv


class TestReadEnv(unittest.TestCase):
    def setUp(self):
        os.environ["MY_VAR"] = "12121"
        self.env_data = "VAR1=value1\nVAR2=value2\nVAR3=12121\n"

        self.temp_dir = tempfile.TemporaryDirectory()
        print("temp dir", self.temp_dir.name)

    def test_read_env(self):
        file_path = os.path.join(self.temp_dir.name, ".env")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.env_data)

        # self.assertEqual(s, "my_value")
        with patch("os.getcwd", return_value=self.temp_dir.name):
            val = GetEnv("MY_VAR").to_float()
            assert val == 12121.0

            val = GetEnv("VAR1").to_str()
            assert val == "value1"

        # Delete the temp file
        os.remove(file_path)

    def test_root_env_file(self):
        subdir_path = os.path.join(self.temp_dir.name, "subdir")
        os.mkdir(subdir_path)

        file_path = os.path.join(subdir_path, ".env")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.env_data)

        with patch("os.getcwd", return_value=subdir_path):
            val = GetEnv("MY_VAR").to_float()
            assert val == 12121.0

            val = GetEnv("VAR1").to_str()
            assert val == "value1"

            val = GetEnv("VAR3").to_int()
            assert val == 12121

        # Delete the temp file
        os.remove(file_path)

    def tearDown(self):
        del os.environ["MY_VAR"]
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
