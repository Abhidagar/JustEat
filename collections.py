"""
Python Data Structures Examples

This module demonstrates the basic usage of Python's built-in data structures:
- List: Ordered, mutable collection
- Tuple: Ordered, immutable collection  
- Set: Unordered collection with unique elements
- Dictionary: Key-value pairs
"""

# List: Ordered, mutable collection 
my_list = [1, 2, 3, "apple"] 
my_list.append("banana")   
print(my_list)   
print(my_list[1])   
 
# Tuple: Ordered, immutable collection 
my_tuple = (10, 20, 30) 
print(my_tuple[0])   
print(my_tuple)   
 
# Set: Unordered, unique elements 
my_set = {1, 2, 2, 3} 
my_set.add(4)   
print(my_set)   
print(2 in my_set)  # Check membership: True 
 
# Dictionary: Key-value pairs 
my_dict = {"name": "Alice", "age": 25} 
my_dict["city"] = "Paris"  # Add key-value pair 
print(my_dict)  
print(my_dict["name"])  # Access value: Alice