import time

# 装饰器，用于测量函数执行时间
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 开始时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 结束时间
        print(f"{func.__name__} execution time: {end_time - start_time} seconds")  # 打印执行时间
        return result
    return wrapper

# 应用装饰器到函数
@time_decorator
def add(a, b):
    return a + b

@time_decorator
def read_and_write(a, b):
    with open('input.txt', 'r') as file:
        file_values = file.read().split()
        a = int(file_values[0])
        b = int(file_values[1])
    return add(a, b)  # 返回 add函数的结果

# 测试函数
if __name__ == "__main__":
    # 从文件读取两个数，计算和，并将结果写入文件
    result = read_and_write(10, 20)  # 存储read_and_write函数的返回值
    print(f"Sum: {result}")  # 打印结果