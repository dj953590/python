import unittest
from utils.configloader import loadconfig

class TestConfigLoader(unittest.TestCase):
    def test_loadconfig(self):
        # Test loading the config
        config = loadconfig()
        print(config)
        self.assertIsNotNone(config)

if __name__ == '__main__':
    unittest.main()