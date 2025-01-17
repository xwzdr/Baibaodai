def filter_array(filter_func, string_array):
    return list(filter(filter_func, string_array))

# Sample Filter Functions
strings = ["hello", "apple", "world", "a test", "python", "code"]

# Excluding strings containing spaces
print(filter_array(lambda x: ' ' not in x, strings))

# Excluding strings starting with the letter "a"
print(filter_array(lambda x: not x.startswith('a'), strings))

# Exclude strings less than 5
print(filter_array(lambda x: len(x) >= 5, strings))
