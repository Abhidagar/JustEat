"""
This script demonstrates how to manually iterate over a list using an iterator object.
"""

numbers = [1, 2, 3]
it = iter(numbers)       # Create an iterator from the list

"""
Use next() to retrieve elements one by one from the iterator.
Each call to next(it) returns the next item in the sequence.
"""

print(next(it))  
print(next(it))  
print(next(it))  
 