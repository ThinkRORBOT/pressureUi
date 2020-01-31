import unittest
import receive_data

class MyTest(unittest.TestCase):
    def test_data_leak(self):
        data_1 = [0.1, 0.15, 0.14, 0.16, 0.29, 0.3, 4, 5, 6, 7, 8 , 8, 9.6, 13, 13.2, 13.3, 13.6, 13.2, 13.1, 13.0, 12.9, 12.8, 12.9, 13.0, 12.7, 12.6, 12.4, 12.6, 12.4, 12.3, 12.2, 12, 11.9, 12.1, 11.8, 11.7]
        test_1 = receive_data.leak_check(5, 3)
        self.assertEqual(test_1.test_list(data_1), True)
    def test_data_nonleak(self):
        data_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12.2, 12.4, 12.3, 12.2, 12.3, 12.5, 12.6, 12.5, 12.6, 12.7, 12.8, 12.5, 12.7, 12.8, 13, 13.1, 13.2, 13.3]
        test_2 = receive_data.leak_check(5, 3)

        self.assertEqual(test_2.test_list(data_2), False)

if __name__ == '__main__':
    unittest.main()
