from collections import deque

class Node:
    """
    A class to represent a node in a binary tree.
    """
    def __init__(self, data):
        self.data = int(data)
        self.left = None
        self.right = None


class Solution:
    def __init__(self):
        self.max_sum = float('-inf')

    def maxPathSum(self, root):
        """
        Calculates the maximum path sum in the binary tree.

        Time Complexity:
            O(n) – Each node is visited once.

        Space Complexity:
            O(h) – Where h is the height of the tree (due to recursion stack).
        """
        def helper(node):
            if not node:
                return 0

            # Calculate left and right max path sums (ignore negatives)
            left_gain = max(helper(node.left), 0)
            right_gain = max(helper(node.right), 0)

            # Update current path sum including both children
            current_path = node.data + left_gain + right_gain

            # Update global maximum if needed
            self.max_sum = max(self.max_sum, current_path)

            # Return one side path for further parent computation
            return node.data + max(left_gain, right_gain)

        helper(root)
        return self.max_sum


def build_tree():
    """
    Builds a binary tree based on user input using level-order (BFS) approach.

    Returns:
        Node: The root of the constructed binary tree.

    Time Complexity:
        O(n) – Each node is processed once.

    Space Complexity:
        O(n) – Queue may store up to n/2 nodes in worst case (last level).
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


# ----------- Main Execution -----------
if __name__ == "__main__":
    print("Enter tree nodes in level order (use 'N' for null):")

    root = build_tree()

    sol = Solution()
    print("Maximum Path Sum:", sol.maxPathSum(root))


"""
============================
Overall File Complexities
============================

Time Complexity:
---------------
- Tree construction: O(n)
- Maximum Path Sum computation: O(n)
- Total: O(n), where n is the number of nodes in the tree.

Space Complexity:
----------------
- Tree construction (queue): O(n)
- Recursion stack (depth = height): O(h)
- Total: O(n) in worst case (for skewed tree).
"""
