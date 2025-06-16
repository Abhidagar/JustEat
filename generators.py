def count_up_to(n):
    """
    A generator that yields numbers from 1 up to (and including) n.

    Parameters:
    -----------
    n : int
        The maximum number to count up to.

    Yields:
    -------
    int
        The next number in the sequence from 1 to n.
    """
    num = 1
    while num <= n:
        yield num
        num += 1

# Unlike lists, this generator doesn’t store all values — it yields one at a time.
gen = count_up_to(3)
print(next(gen))  
print(next(gen))  
print(next(gen))  
