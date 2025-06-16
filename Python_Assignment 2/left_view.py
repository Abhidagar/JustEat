from collections import deque

# Node class for the Binary Tree
class Node:
    """
    A class to represent a node in a binary tree.

    Attributes:
        data (int): The value of the node.
        left (Node): Pointer to the left child node.
        right (Node): Pointer to the right child node.
    """
    def __init__(self, data):
        """
        Initializes a node with given data, and sets left and right children to None.

        Args:
            data (int): Value to be stored in the node.
        """
        self.data = data
        self.left = None
        self.right = None


def build_tree():
    """
    Builds a binary tree based on user input using level-order (BFS) approach.

    Returns:
        Node: The root of the constructed binary tree.

    Time Complexity:
        O(n) — each node is visited exactly once.

    Space Complexity:
        O(n) — for the queue used in level-order traversal.
    """
    val = input("Enter root node value: ")
    if val == "None":
        return None
    root = Node(int(val))
    queue = deque([root])  # queue to build tree level by level

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


def print_left_view(root):
    """
    Prints the left view of a binary tree.

    The left view contains the first node at each level when viewed from the left side.

    Args:
        root (Node): The root node of the binary tree.

    Time Complexity:
        O(n) — level-order traversal visits every node once.

    Space Complexity:
        O(w) — where w is the maximum width of the tree (maximum number of nodes at any level).
    """
    if not root:
        return
    queue = deque([root])  # For level order traversal

    while queue:
        level_length = len(queue)
        for i in range(level_length):
            node = queue.popleft()
            if i == 0:
                print(node.data, end=' ')  # First node at this level → left view
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


# Run the functions
root = build_tree()
print("Left View of Tree:")
print_left_view(root)

"""
============================
 Overall File Complexities
============================

Time Complexity:
---------------
- build_tree: O(n) — each node inserted based on input
- print_left_view: O(n) — each node visited once
- Total: O(n)

Space Complexity:
----------------
- Queue in both build_tree and print_left_view: O(n)
- Total: O(n)
"""
