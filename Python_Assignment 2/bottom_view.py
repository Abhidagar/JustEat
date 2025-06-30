from collections import deque
from tree_utils import Node, build_tree

def bottom_view(root):
    """
    Prints the bottom view of the binary tree.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return

    q = deque()
    hd_map = dict()  # Horizontal Distance -> Node.data

    root.level = 0
    q.append(root)

    while q:
        node = q.popleft()
        level = node.level

        # Always update the latest node at this horizontal distance
        hd_map[level] = node.data

        if node.left:
            node.left.level = level - 1
            q.append(node.left)

        if node.right:
            node.right.level = level + 1
            q.append(node.right)

    for key in sorted(hd_map.keys()):
        print(hd_map[key], end=" ")

# -------- Main Execution --------
if __name__ == "__main__":
    root = build_tree()
    print("Bottom view of the binary tree:")
    bottom_view(root)
