from collections import deque

# Binary Tree Node class
class Node:
    """
    Represents a node in a binary tree.

    Attributes:
        data (int): The value of the node.
        left (Node): The left child node.
        right (Node): The right child node.
    """
    def __init__(self, data):
        """
        Initializes a new node with the given data.

        Args:
            data (int): Value to be stored in the node.
        """
        self.data = data
        self.left = None
        self.right = None


def build_tree():
    """
    Builds a binary tree based on user input in level-order format.

    Returns:
        Node: The root of the constructed binary tree.

    Time Complexity:
        O(n) — where n is the number of nodes in the binary tree (each node is created once).

    Space Complexity:
        O(n) — due to queue usage in level-order traversal.
    """
    val = input("Enter root node value: ")
    if val == "None":
        return None
    root = Node(int(val))
    queue = deque([root])  # Queue for level order building

    while queue:
        current = queue.popleft()

        left_val = input(f"Enter left child of {current.data} (None if no child): ")
        if left_val != "None":
            current.left = Node(int(left_val))
            queue.append(current.left)

        right_val = input(f"Enter right child of {current.data} (None if no child): ")
        if right_val != "None":
            current.right = Node(int(right_val))
            queue.append(current.right)

    return root


def print_right_view(root):
    """
    Prints the right view of a binary tree.

    The right view includes the last node at each level when the tree is viewed from the right side.

    Args:
        root (Node): The root node of the binary tree.

    Time Complexity:
        O(n) — every node is visited once using level-order traversal.

    Space Complexity:
        O(w) — where w is the maximum width of the tree (maximum number of nodes at any level).
    """
    if not root:
        return
    queue = deque([root])  # Queue for level order traversal

    while queue:
        level_length = len(queue)
        for i in range(level_length):
            node = queue.popleft()
            if i == level_length - 1:  # Last node at this level → right view
                print(node.data, end=' ')
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


# Main execution
root = build_tree()
print("Right View of Tree:")
print_right_view(root)

"""
============================
 Overall File Complexities
============================

Time Complexity:
---------------
- build_tree: O(n) — input and construction of n nodes
- print_right_view: O(n) — one visit per node
- Total: O(n)

Space Complexity:
----------------
- Queue in both build_tree and print_right_view: O(n) worst case
- Total: O(n)
"""