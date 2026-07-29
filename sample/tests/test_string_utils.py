"""miniqa 用例示例（二）：演示如何给「新模块」补测试，全部用函数式 @test 写法。"""
from miniqa import test, assert_equal, assert_true
from sample.app.string_utils import reverse, is_palindrome, count_vowels


@test
def test_reverse():
    assert_equal(reverse("hello"), "olleh")


@test
def test_reverse_empty():
    assert_equal(reverse(""), "")


@test
def test_is_palindrome():
    assert_true(is_palindrome("Level"))
    assert_true(is_palindrome("上海自来水来自海上"))


@test
def test_count_vowels():
    assert_equal(count_vowels("aeiou"), 5)
    assert_equal(count_vowels("bcdfg"), 0)
