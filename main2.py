def filter_array(filter_func, string_array):
    return list(filter(filter_func, string_array))

# 示例过滤函数
strings = ["hello", "apple", "world", "a test", "python", "code"]

# 排除包含空格的字符串
print(filter_array(lambda x: ' ' not in x, strings))

# 排除以字母“a”开头的字符串
print(filter_array(lambda x: not x.startswith('a'), strings))

# 排除长度小于 5 的字符串
print(filter_array(lambda x: len(x) >= 5, strings))
