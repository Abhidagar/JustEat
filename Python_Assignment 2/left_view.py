from collections import deque
from tree_utils import Node, build_tree
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

