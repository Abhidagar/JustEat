# Function with parameter passing and return value
def fibonacci(n):
    """
    Recursively calculates the nth Fibonacci number.

    Parameters:
    -----------
    n : int
        The position in the Fibonacci sequence (0-indexed).

    Returns:
    --------
    int
        The nth Fibonacci number.
    """
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Function with default parameter
def multiply(number, factor=2):
    """
    Multiplies a number by a given factor.

    Parameters:
    -----------
    number : int or float
        The number to be multiplied.
    factor : int or float, optional
        The factor by which to multiply (default is 2).

    Returns:
    --------
    int or float
        The product of number and factor.
    """
    return number * factor

# Example usage
print(multiply(5))     