import importlib
import os
import tempfile
import unittest
from unittest.mock import patch

import newenvreader


class TestEnvParsing(unittest.TestCase):
    def setUp(self):
        os.environ["MY_VAR"] = "12121"
        os.environ["KEY_NOT_OVERRIDDEN_BY_ENV"] = "Normal"

        env_data = """
        [settings]
        STR_VAL=value1
        StrVal=value2
        INT_VAL=12121
        FLOAT_VAL=32.1234
        COMPL_VAL=postgresql://user:pass@localhost:5432/db

        KeyTrue=True
        KeyOne=1
        KeyYes=yes
        KeyY=y
        KeyOn=on

        KeyFalse=False
        KeyZero=0
        KeyNo=no
        KeyN=n
        KeyOff=off
        KeyEmpty=

        #CommentedKey=None
        PERCENT_ESCAPED=%%
        INTERPOLATION=%(KeyOff)s
        IGNORE_SPACE = text
        KEY_NOT_OVERRIDDEN_BY_ENV=Overide
        """

        self.temp_dir = tempfile.TemporaryDirectory()
        file_path = os.path.join(self.temp_dir.name, "settings.ini")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(env_data)

        with patch("os.getcwd", return_value=self.temp_dir.name):
            importlib.reload(newenvreader)
        self.file_path = file_path

    def test_env_normal(self):
        assert newenvreader.get_env("MY_VAR", cast=int) == 12121
        assert newenvreader.get_env("STR_VAL") == "value1"
        assert newenvreader.get_env("StrVal") == "value2"
        assert newenvreader.get_env("INT_VAL") == "12121"
        assert (
            newenvreader.get_env("COMPL_VAL")
            == "postgresql://user:pass@localhost:5432/db"
        )

    def test_env_bool_casting(self):
        assert newenvreader.get_env("KeyTrue", cast=bool) is True
        assert newenvreader.get_env("KeyOne", cast=bool) is True
        assert newenvreader.get_env("KeyYes", cast=bool) is True
        assert newenvreader.get_env("KeyY", cast=bool) is True
        assert newenvreader.get_env("KeyOn", cast=bool) is True
        assert newenvreader.get_env("KeyFalse", cast=bool) is False
        assert newenvreader.get_env("KeyZero", cast=bool) is False
        assert newenvreader.get_env("KeyNo", cast=bool) is False
        assert newenvreader.get_env("KeyN", cast=bool) is False
        assert newenvreader.get_env("KeyOff", cast=bool) is False
        assert newenvreader.get_env("KeyEmpty", cast=bool) is False

    def test_env_int_casting(self):
        assert newenvreader.get_env("INT_VAL", cast=int) == 12121
        assert newenvreader.get_env("VAR11", default=12, cast=int) == 12
        # Check for exception
        with self.assertRaises(ValueError):
            newenvreader.get_env("STR_VAL", cast=int)

    def test_env_val_edges(self):
        with self.assertRaises(KeyError):
            newenvreader.get_env("COMMENTED_KEY")

        assert newenvreader.get_env("PERCENT_ESCAPED") == "%"
        assert newenvreader.get_env("INTERPOLATION") == 'off'
        assert newenvreader.get_env("IGNORE_SPACE") == "text"
        assert newenvreader.get_env("KEY_NOT_OVERRIDDEN_BY_ENV") == "Overide"

    def tearDown(self):
        del os.environ["MY_VAR"]
        del os.environ["KEY_NOT_OVERRIDDEN_BY_ENV"]
        os.remove(self.file_path)
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
