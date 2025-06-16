"""
This script demonstrates various types of Python operators:
1. Arithmetic Operators
2. Comparison Operators
3. Logical Operators
4. Bitwise Operators
"""

# === 1. Arithmetic Operators ===
a = 10
b = 3

"""
Arithmetic operations between integers a and b.
Includes addition, subtraction, multiplication, division,
modulus, and exponentiation.
"""
print("Arithmetic Operators:")
print(f"{a} + {b} = {a + b}")     # Addition
print(f"{a} - {b} = {a - b}")     # Subtraction
print(f"{a} * {b} = {a * b}")     # Multiplication
print(f"{a} / {b} = {a / b}")     # Division
print(f"{a} % {b} = {a % b}")     # Modulus
print(f"{a} ** {b} = {a ** b}")   # Exponentiation

print("\n")

# === 2. Comparison Operators ===
"""
Comparison operations to evaluate relational expressions between a and b.
"""
print("Comparison Operators:")
print(f"{a} == {b}: {a == b}")
print(f"{a} != {b}: {a != b}")
print(f"{a} > {b}: {a > b}")
print(f"{a} < {b}: {a < b}")
print(f"{a} >= {b}: {a >= b}")
print(f"{a} <= {b}: {a <= b}")

print("\n")

# === 3. Logical Operators ===
x = True
y = False

"""
Logical operations between Boolean values x and y.
"""
print("Logical Operators:")
print(f"x and y: {x and y}")
print(f"x or y: {x or y}")
print(f"not x: {not x}")

print("\n")

# === 4. Bitwise Operators ===
m = 5   # Binary: 0101
n = 3   # Binary: 0011

"""
Bitwise operations between integers m and n.
Includes AND, OR, XOR, NOT, left shift, and right shift.
"""
print("Bitwise Operators:")
print(f"{m} & {n} = {m & n}")     # AND
print(f"{m} | {n} = {m | n}")     # OR
print(f"{m} ^ {n} = {m ^ n}")     # XOR
print(f"~{m} = {~m}")             # NOT
print(f"{m} << 1 = {m << 1}")     # Left shift
print(f"{m} >> 1 = {m >> 1}")     # Right shift


