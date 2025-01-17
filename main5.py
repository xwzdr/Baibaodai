import time

# Decorator to measure function execution time
def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Starting time
        result = func(*args, **kwargs)  # executable function
        end_time = time.time()  # end time
        print(f"{func.__name__} execution time: {end_time - start_time} seconds")  # Print execution time
        return result
    return wrapper

# Applying Decorators to Functions
@time_decorator
def add(a, b):
    return a + b

@time_decorator
def read_and_write(a, b):
    with open('input.txt', 'r') as file:
        file_values = file.read().split()
        a = int(file_values[0])
        b = int(file_values[1])
    return add(a, b)  # Returns the result of the add function

# test function
if __name__ == "__main__":
    # Reads two numbers from a file, calculates the sum, and writes the result to the file
    result = read_and_write(10, 20)  # Storing the return value of the read_and_write function
    print(f"Sum: {result}")  # Print results
