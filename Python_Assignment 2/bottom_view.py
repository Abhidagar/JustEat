class Node:
    """
    A class to represent a node in a binary tree.

    Attributes:
        data (int): The value stored in the node.
        left (Node): The left child node.
        right (Node): The right child node.
        level (int): Horizontal distance from the root (used for view calculations).
    """
    def __init__(self, data):
        """
        Initializes a node with data, left and right as None, and level as None.

        Args:
            data (int): Value to store in the node.
        """
        self.data = data
        self.left = None
        self.right = None
        self.level = None


class BinarySearchTree:
    """
    A class to represent a Binary Search Tree (BST).

    Attributes:
        root (Node): The root node of the BST.
    """
    def __init__(self):
        """Initializes the BST with root set to None."""
        self.root = None

    def create(self, val):
        """
        Inserts a value into the BST following standard rules.

        Args:
            val (int): The value to insert into the BST.

        Time Complexity:
            Best Case: O(log n) — for a balanced tree
            Worst Case: O(n) — for a skewed tree (linked list)

        Space Complexity:
            O(1) — no recursion used, just iterative insert
        """
        if self.root is None:
            self.root = Node(val)
        else:
            current = self.root
            while True:
                if val < current.data:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.data:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break


def bottom_view(root):
    """
    Prints the bottom view of a binary tree.

    Bottom view includes the last (lowest) node at each horizontal level when viewed from the bottom.

    Args:
        root (Node): The root node of the binary tree.

    Time Complexity:
        O(n + k log k)
        - O(n) for traversing all nodes
        - O(k log k) for sorting the horizontal levels (k ≤ n)

    Space Complexity:
        O(n)
        - O(n) for queue (level-order traversal)
        - O(n) for dictionary (to store bottom-most nodes at each level)
    """
    if not root:
        return

    q = []
    d = dict()
    root.level = 0  # Horizontal distance from root
    q.append(root)

    while len(q) != 0:
        root = q.pop(0)
        # Always overwrite to keep the bottom-most node at each level
        d[root.level] = root.data

        if root.left:
            q.append(root.left)
            root.left.level = root.level - 1

        if root.right:
            q.append(root.right)
            root.right.level = root.level + 1

    for i in sorted(d):  # Print from leftmost to rightmost level
        print(d[i], end=' ')


# ----------- Main Execution -----------
if __name__ == "__main__":
    bt = BinarySearchTree()
    values = list(map(int, input("Enter values to insert into Binary Tree: ").split()))

    for val in values:
        bt.create(val)

    print("Bottom View of the Binary Tree:")
    bottom_view(bt.root)

"""
============================
 Overall File Complexities
============================

Time Complexity:
---------------
- BST Insertions: O(n log n) average, O(n²) worst (skewed)
- Bottom View: O(n + k log k) → O(n log n) worst case
- Total Time: O(n log n) average, O(n²) worst

Space Complexity:
----------------
- Dictionary and Queue in bottom view: O(n)
- Total Space: O(n)
"""
