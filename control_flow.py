"""
This script demonstrates:
1. A palindrome checker using if-elif-else.
2. Summing even numbers in a list using a for loop.
3. A simple password checker using a while loop.
"""

# Palindrome Checker
word = input("Enter a word: ")

# Convert to lowercase for case-insensitive comparison (if-elif-else)
if word.lower() == word[::-1].lower():
    """
    Check if the entered word is a palindrome.
    Comparison is case-insensitive.
    """
    print(f"'{word}' is a palindrome.")
elif len(word) < 3:
    """
    Handles case where the word is too short to be considered a valid palindrome.
    """
    print("Word is too short to be a palindrome.")
else:
    """
    Handles case where the word is not a palindrome.
    """
    print(f"'{word}' is not a palindrome.")

# Sum of even numbers in a list (for loop)
numbers = [1, 4, 5, 6, 9, 12, 15, 20]
even_sum = 0

"""
Loop through a list of integers and calculate the sum of all even numbers.
"""
for num in numbers:
    if num % 2 == 0:
        even_sum += num

print("Sum of even numbers:", even_sum)

# While loop for password checking
correct_password = "admin123"
attempts = 3

"""
Allow the user up to 3 attempts to enter the correct password.
If the correct password is entered, access is granted.
If attempts reach 0, account is locked.
"""
while attempts > 0:
    entered = input("Enter your password: ")

    if entered == correct_password:
        print("Access granted.")
        break
    else:
        attempts -= 1
        print(f"Wrong password. {attempts} attempt(s) left.")

if attempts == 0:
    print("Account locked due to too many failed attempts.")
