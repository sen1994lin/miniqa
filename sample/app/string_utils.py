"""被测对象（SUT）：一个字符串小工具，用于演示如何给「新模块」写测试。"""


def reverse(s):
    return s[::-1]


def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]


def count_vowels(s):
    return sum(1 for ch in s.lower() if ch in "aeiou")
