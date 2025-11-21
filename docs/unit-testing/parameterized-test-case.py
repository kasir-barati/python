from unittest import TestCase

def sum(a: int, b: int) -> int:
    return a + b

class TestSumFunction(TestCase):
    def test_sum(self):
        test_cases = [
            (1, 2, 4),
            (-1, 1, 0),
            (0, 0, 0),
            (100, 200, 300),
        ]
        for a, b, expected in test_cases:
            with self.subTest(msg="it should add num1 and num2", params=(a, b, expected)):
                result = sum(a, b)

                self.assertEqual(result, expected)
