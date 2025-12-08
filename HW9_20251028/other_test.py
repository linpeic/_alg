import unittest
# 假設你的主程式檔名叫做 mindistance.py
from mindistance import min_edit_distance 

class TestEditDistance(unittest.TestCase):
    
    def test_basic_example(self):
        # 測試基本案例
        self.assertEqual(min_edit_distance("kitten", "sitting"), 3)
        
    def test_missing_char(self):
        # 測試少一個字
        self.assertEqual(min_edit_distance("kitte", "sitting"), 4)

    def test_empty_string(self):
        # 測試空字串
        self.assertEqual(min_edit_distance("", "abc"), 3)

if __name__ == '__main__':
    unittest.main()