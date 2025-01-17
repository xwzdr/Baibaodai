def is_palindrome(s):
    return s == s[::-1]

# typical example
print(is_palindrome("racecar"))  # True
print(is_palindrome("hello"))    # False
