from collections import deque
from tree_utils import Node, build_tree


def print_alternate_levels(root):
    """
    Prints the values of the binary tree nodes from alternate levels
    (starting with level 0 — the root).

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return

    queue = deque()
    queue.append(root)
    level = 0

    while queue:
        level_size = len(queue)
        current_level_values = []

        for _ in range(level_size):
            node = queue.popleft()

            if level % 2 == 0:  # Print only even-numbered levels (0, 2, 4,...)
                current_level_values.append(node.data)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if current_level_values:
            print(" ".join(map(str, current_level_values)), end=" ")

        level += 1

# -------- Main Execution --------
if __name__ == "__main__":
    root = build_tree()
    print("Values from alternate levels (1st, 3rd, 5th, ...):")
    print_alternate_levels(root)
