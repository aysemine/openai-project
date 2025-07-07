from langchain.tools import tool

@tool
def calculator(a: float, b:float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a+b}"