import unittest
from utils import configloader as cl

class TestConfigLoader(unittest.TestCase):
    def test_loadconfig(self):
        # Test loading the config
        config = cl.loadconfig()
        print(config)
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main()