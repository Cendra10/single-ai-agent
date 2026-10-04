from datetime import datetime

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


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform a mathematical operation on two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "divide", "multiply"]
                    },
                    "a": {
                        "type": "number"
                    },
                    "b": {
                        "type": "number"
                    }
                },
                "required": ["operation", "a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]