def wrapper(func):
    """
    A decorator function that wraps another function to add
    a greeting before and a goodbye message after its execution.

    Parameters:
    -----------
    func : function
        The function to be wrapped.

    Returns:
    --------
    function
        The modified inner function with additional behavior.
    """
    def inner():
        """Inner function that adds pre- and post-execution messages."""
        print("Hello!")
        func()
        print("Goodbye!")
    return inner

@wrapper
def say_hello():
    """
    A simple function that prints an introduction message.
    """
    print("My name is Python.")

# Call the decorated function
say_hello()