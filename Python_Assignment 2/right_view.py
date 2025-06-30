from collections import deque
from tree_utils import Node, build_tree
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

