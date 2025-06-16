class BankAccount:
    """
    A class to represent a simple bank account.

    Attributes:
    -----------
    owner : str
        Name of the account holder.
    balance : float
        Current account balance.

    Methods:
    --------
    deposit(amount):
        Deposits the given amount into the account after validating it.
    withdraw(amount):
        Withdraws the given amount from the account after validating it.
    """

    def __init__(self, owner, balance=0):
        """
        Initializes a new BankAccount object.

        Parameters:
        -----------
        owner : str
            The name of the account holder.
        balance : float, optional
            Initial account balance (default is 0).
        """
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits a specified amount into the account.

        Parameters:
        -----------
        amount : float
            The amount to deposit. Must be positive.

        Raises:
        -------
        ValueError:
            If the amount is not greater than zero.

        Behavior:
        ---------
        - Prints success message if deposit is valid.
        - Prints error message if deposit is invalid.
        - Always prints that the deposit operation has completed.
        """
        print("\n Deposit Operation Started")
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
        except ValueError as e:
            print(f" Error: {e}")
        else:
            self.balance += amount
            print(f" Deposited ₹{amount}. New balance: ₹{self.balance}")
        finally:
            print("ℹ Deposit operation completed.")

    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account.

        Parameters:
        -----------
        amount : float
            The amount to withdraw. Must not exceed current balance.

        Raises:
        -------
        ValueError:
            If the withdrawal amount is greater than the current balance.

        Behavior:
        ---------
        - Prints success message if withdrawal is valid.
        - Prints error message if withdrawal is invalid.
        - Always prints that the withdrawal operation has completed.
        """
        print("\n Withdraw Operation Started")
        try:
            if amount > self.balance:
                raise ValueError("Insufficient balance.")
        except ValueError as e:
            print(f" Error: {e}")
        else:
            self.balance -= amount
            print(f" Withdrew ₹{amount}. Remaining balance: ₹{self.balance}")
        finally:
            print("ℹ Withdrawal operation completed.")


# Testing the class
account = BankAccount("Rahul", 1000)

account.deposit(500)     
account.deposit(-200)     
account.withdraw(300)     
account.withdraw(2000)    