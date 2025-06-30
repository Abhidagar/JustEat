from collections import deque
from tree_utils import Node , build_tree

def top_view(root):
    """
    Prints the top view of a binary tree.

    The top view includes the first node visible from the top at each horizontal distance.

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

        if level not in hd_map:
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
    print("Top view of the binary tree:")
    top_view(root)
