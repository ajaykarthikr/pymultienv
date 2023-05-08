import unittest
import os

from src.typedenv.main import get_env


class TestReadEnv(unittest.TestCase):
    
    def setUp(self):
        os.environ['MY_VAR'] = 'my_value'

    def test_read_env(self):
        s = get_env('TEST')
        print(s)
        self.assertEqual(s, 'my_value')

    def tearDown(self):
        del os.environ['MY_VAR']


if __name__ == '__main__':
    unittest.main()
