import importlib
import os
import tempfile
import unittest
from unittest.mock import patch

import newenvreader

class TestReadEnv(unittest.TestCase):
    def setUp(self):
        os.environ["MY_VAR"] = "12121"
        self.env_data = "VAR1=value1\nVAR2=value2\nVAR3=12121\n"

        self.temp_dir = tempfile.TemporaryDirectory()

    def test_read_env(self):

        file_path = os.path.join(self.temp_dir.name, ".env")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self.env_data)

        with patch("os.getcwd", return_value=self.temp_dir.name):
            importlib.reload(newenvreader)
            
            val = newenvreader.get_env("MY_VAR", cast=int)
            assert val == 12121.0

            val = newenvreader.get_env("VAR1")
            assert val == "value1"

            val = newenvreader.get_env("VAR1")
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
            importlib.reload(newenvreader)
            
            val = newenvreader.get_env("MY_VAR", cast=float)
            assert val == 12121.0

            val = newenvreader.get_env("VAR1")
            assert val == "value1"

            val = newenvreader.get_env("VAR3", cast=int)
            assert val == 12121

        # Delete the temp file
        os.remove(file_path)

    def tearDown(self):
        del os.environ["MY_VAR"]
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
