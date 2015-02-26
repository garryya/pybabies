#!/usr/bin/python

import sys

class RomanConverter:

    _romanNumbersLAT = {
        'I' : 1,
        'V' : 5,
        'X' : 10,
        'L' : 50,
        'C' : 100,
        'D' : 500,
        'M' : 1000,
        'v' : 5000,
        'x' : 10000,
        'l' : 50000,
        'c' : 100000,
        'd' : 500000,
        'm' : 1000000,
    }
    _romanNumbersRLAT = { v:k for k,v in _romanNumbersLAT.items() }

    _ONE = 'O'
    _FIVE = 'F'
    _TEN = 'T'

    _romanDigitsMnemonicLAT = {
        1 : _ONE*1,
        2 : _ONE*2,
        3 : _ONE*3,
        4 : _ONE + _FIVE,
        5 : _FIVE,
        6 : _FIVE + _ONE*1,
        7 : _FIVE + _ONE*2,
        8 : _FIVE + _ONE*3,
        9 : _ONE + _TEN
    }
    _romanDigitsMnemonicRLAT = { v:k for k,v in _romanDigitsMnemonicLAT.items() }

    def __init__(self):
        pass

    def _decodeRomanMnemonic(self, mnemonicDigit, npos):
        one = self._romanNumbersRLAT[10**npos]
        five = self._romanNumbersRLAT[10**npos*5]
        ten = self._romanNumbersRLAT[10**(npos+1)]
        return mnemonicDigit.replace(self._ONE,one).replace(self._FIVE,five).replace(self._TEN,ten)

    def _decimal2roman_digit(self, digit, npos):
        return self._decodeRomanMnemonic(self._romanDigitsMnemonicLAT[digit], npos)

    def decimal2roman(self, n, npos=0):
        roman_number = ''
        if n/10:
            roman_number = self.decimal2roman(n/10, npos+1)
        roman_number = roman_number + self._decimal2roman_digit(n % 10, npos)
        return roman_number


    def roman2decimal(self, roman_number, npos=0):
        roman_digit = ''
        length = len(roman_number)
        decodedRomanDigitsRLAT = { self._decodeRomanMnemonic(k,npos):v for k,v in self._romanDigitsMnemonicRLAT.items() }
        for i in reversed(range(length)):
            if roman_number[i]+roman_digit not in decodedRomanDigitsRLAT:
                break
            roman_digit = roman_number[i] + roman_digit
        decimal_number = 0
        if i > 0:
            decimal_number = self.roman2decimal(roman_number[:i+1], npos+1)
        if roman_digit:
            decimal_number += decodedRomanDigitsRLAT[roman_digit] * 10**npos
        return decimal_number


    def isDecimalNumber(self, numstr):
        try:
            return int(numstr)
        except ValueError:
            return False

    def isRomanNumber(self, numstr):
        return all(map(lambda s:s in self._romanNumbersLAT, numstr))


rc = RomanConverter()

print 'Number -> ',
numstr = sys.stdin.readline().strip()
print

if rc.isRomanNumber(numstr):
    print 'Converting roman to decimal --> %s = %s' % (numstr, rc.roman2decimal(numstr))
elif rc.isDecimalNumber(numstr):
    print 'Converting decimal to roman --> %s = %s' % (numstr, rc.decimal2roman(int(numstr)))
else:
    print 'Uknown number'

