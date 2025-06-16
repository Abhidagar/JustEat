class Node:
    """
    Represents a node in a binary tree.

    Attributes:
        data (int): The value stored in the node.
        left (Node): The left child node.
        right (Node): The right child node.
    """
    def __init__(self, data):
        """
        Initializes the node with data and sets left and right to None.

        Args:
            data (int): The value to store in the node.
        """
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Represents a Binary Search Tree (BST).

    Attributes:
        root (Node): The root of the BST.
    """
    def __init__(self):
        """Initializes an empty BST with root as None."""
        self.root = None

    def create(self, data):
        """
        Inserts a value into the BST.

        Args:
            data (int): The value to insert.

        Time Complexity:
            O(log n) on average for balanced BST, O(n) in worst case (skewed tree).
        
        Space Complexity:
            O(1) per insertion (excluding recursion stack, which is O(h) = tree height).
        """
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(self.root, data)

    def _insert(self, node, data):
        """
        Helper method to insert a value into the BST recursively.

        Args:
            node (Node): The current node in traversal.
            data (int): The value to insert.
        """
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(node.left, data)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(node.right, data)

    def print_alternate_levels(self, root):
        """
        Prints the values of nodes at alternate levels (1st, 3rd, 5th, etc.) of the tree.

        Args:
            root (Node): The root of the binary tree.

        Time Complexity:
            O(n) — all nodes are visited level by level.

        Space Complexity:
            O(w) — where w is the max number of nodes at any level (width of tree), due to queue usage.
        """
        if not root:
            return

        q = []
        level = 1  # Start with level 1
        root.level = level
        q.append(root)

        while len(q) != 0:
            level_size = len(q)  # Number of nodes at current level
            current_level = q[0].level  # Get current level number

            # Process all nodes at current level
            for i in range(level_size):
                node = q.pop(0)

                # Print only odd levels (1st, 3rd, 5th, etc.)
                if current_level % 2 == 1:
                    print(node.data, end=' ')

                # Add children to queue with next level
                if node.left:
                    node.left.level = current_level + 1
                    q.append(node.left)

                if node.right:
                    node.right.level = current_level + 1
                    q.append(node.right)

            # Print newline after each alternate level for better readability
            if current_level % 2 == 1 and len(q) > 0:
                print()  # New line after printing an alternate level


# ----------- Main Execution -----------
if __name__ == "__main__":
    bt = BinarySearchTree()
    values = list(map(int, input("Enter values to insert into Binary Tree: ").split()))

    for val in values:
        bt.create(val)

    print("Alternate Level Values (1st, 3rd, 5th, etc.):")
    bt.print_alternate_levels(bt.root)

"""
============================
 Overall File Complexities
============================

Time Complexity:
---------------
- Insertion (create): O(n log n) on average for n nodes in balanced BST, O(n^2) in worst case.
- print_alternate_levels: O(n) — all nodes are visited.
- Total: O(n log n) average, O(n^2) worst case.

Space Complexity:
----------------
- Queue in print_alternate_levels: O(w), where w = max width of tree.
- Recursive stack for insertion: O(h), h = height of tree.
- Total: O(n) in worst case for unbalanced tree.
"""
