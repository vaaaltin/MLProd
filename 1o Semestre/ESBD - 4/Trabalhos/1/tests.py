import unittest
from roman_to_integer import RomanToInteger

class RomanToIntegerTests(unittest.TestCase):
    def test_single_digit(self):
        self.assertEqual(RomanToInteger.romanToInt('I'), 1)
        self.assertEqual(RomanToInteger.romanToInt('V'), 5)
        self.assertEqual(RomanToInteger.romanToInt('X'), 10)
        self.assertEqual(RomanToInteger.romanToInt('L'), 50)
        self.assertEqual(RomanToInteger.romanToInt('C'), 100)
        self.assertEqual(RomanToInteger.romanToInt('D'), 500)
        self.assertEqual(RomanToInteger.romanToInt('M'), 1000)

    def test_two_digits(self):
        self.assertEqual(RomanToInteger.romanToInt('IV'), 4)
        self.assertEqual(RomanToInteger.romanToInt('IX'), 9)
        self.assertEqual(RomanToInteger.romanToInt('XL'), 40)
        self.assertEqual(RomanToInteger.romanToInt('XC'), 90)
        self.assertEqual(RomanToInteger.romanToInt('CD'), 400)
        self.assertEqual(RomanToInteger.romanToInt('CM'), 900)

    def test_multiple_digits(self):
        self.assertEqual(RomanToInteger.romanToInt('III'), 3)
        self.assertEqual(RomanToInteger.romanToInt('VIII'), 8)
        self.assertEqual(RomanToInteger.romanToInt('XII'), 12)
        self.assertEqual(RomanToInteger.romanToInt('XXV'), 25)
        self.assertEqual(RomanToInteger.romanToInt('XLIV'), 44)
        self.assertEqual(RomanToInteger.romanToInt('XCIX'), 99)
        self.assertEqual(RomanToInteger.romanToInt('CDLIX'), 459)
        self.assertEqual(RomanToInteger.romanToInt('CMXCIX'), 999)
        self.assertEqual(RomanToInteger.romanToInt('MMMCMXCIX'), 3999)
    
    def test_sequence_four_equal(self):
        self.assertEqual(RomanToInteger.romanToInt('IIII'), 'NA')
        self.assertEqual(RomanToInteger.romanToInt('IVIIII'),'NA')

    def test_sequence_bigger_after(self):
        self.assertEqual(RomanToInteger.romanToInt('DM'), 'NA')

if __name__ == '__main__':
    unittest.main()