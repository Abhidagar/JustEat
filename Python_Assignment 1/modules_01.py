"""
math_utils.py

A simple utility module for basic mathematical operations.
"""

def square(num):
    """
    Returns the square of a number.

    Parameters:
    -----------
    num : int or float
        The number to square.

    Returns:
    --------
    int or float
        The square of the input number.
    """
    return num * num


def cube(num):
    """
    Returns the cube of a number.

    Parameters:
    -----------
    num : int or float
        The number to cube.

    Returns:
    --------
    int or float
        The cube of the input number.
    """
    return num ** 3


def is_even(num):
    """
    Checks if a number is even.

    Parameters:
    -----------
    num : int
        The number to check.

    Returns:
    --------
    bool
        True if the number is even, False otherwise.
    """
    return num % 2 == 0
