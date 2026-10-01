def calculator(operation, a, b):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b
    elif operation == "multiply":
        return a * b
    else:
        return "Unknown operation occurred."

if __name__ == "__main__":
    print(calculator("add", 2, 3))
    print(calculator("subtract", 10, 5))
    print(calculator("divide", 10, 0))
    print(calculator("multiply", 2, 3))
    print(calculator("modulo", 7, 2))