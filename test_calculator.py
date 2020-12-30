import unittest
import calculator


class TestCalculator(unittest.TestCase):

    def test_calculation(self):
        self.assertEqual(8, calculator.count("8"))
        self.assertEqual(3, calculator.count("-2 + 4 - 5 + 6"))
        self.assertEqual(27, calculator.count("9 +++ 10 -- 8"))
        self.assertEqual(-2, calculator.count("3 --- 5"))
        self.assertEqual(2, calculator.count("14       -   12"))
        self.assertEqual(12, calculator.count("7 + 1 + 4"))
        self.assertEqual(5, calculator.count("5"))