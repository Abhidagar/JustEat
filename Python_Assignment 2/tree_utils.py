from collections import deque
class Node:
    """
    Represents a node in the binary tree.
    """
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.data)

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
    val = input("Enter root node value (or 'None'): ")
    if val == "None":
        return None
    
    root = Node(int(val))
    queue = deque([root])

    while queue:
        current = queue.popleft()

        left_val = input(f"Enter left child of {current.data} (or 'None'): ")
        if left_val != "None":
            current.left = Node(int(left_val))
            queue.append(current.left)

        right_val = input(f"Enter right child of {current.data} (or 'None'): ")
        if right_val != "None":
            current.right = Node(int(right_val))
            queue.append(current.right)

    return root