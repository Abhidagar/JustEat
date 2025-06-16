class Node:
    """
    Represents a node in a binary tree.

    Attributes:
        data (int): Value stored in the node.
        left (Node): Left child.
        right (Node): Right child.
        level (int): Horizontal distance from root for top view logic.
    """
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.level = None  # Used only in top view


class BinarySearchTree:
    """
    A binary search tree with insertion and top view functionality.
    """
    def __init__(self):
        self.root = None

    def create(self, val):
        """
        Inserts a value into the binary search tree.

        Time Complexity:
            - Average Case: O(log N) for balanced tree
            - Worst Case: O(N) for skewed tree (e.g. sorted input)

        Space Complexity:
            - O(1) auxiliary (no recursion or extra data structures)
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
                        current.right = Node(val)
                        break
                    else:
                        current = current.right
                else:
                    break  # No duplicates


    def top_view(root):
        """
        Prints the top view of the binary tree using level-order traversal (BFS).

        Top view includes the first visible node at each horizontal distance from the root.

        Approach:
            - Perform BFS (level-order) traversal.
            - Track horizontal levels using a 'level' attribute.
            - Store first node seen at each horizontal level in a dictionary.
            - Finally, print the nodes in order of increasing level (left to right).

        Time Complexity:
            - Visiting all N nodes: O(N)
            - Sorting horizontal levels: O(N log N) in worst-case (skewed tree)
            - Overall: O(N log N)

        Space Complexity:
            - Queue: O(N) in the worst case (last level holds ~N/2 nodes)
            - Dictionary: O(N) for N horizontal distances
        """
        if not root:
            return

        q = []           # For BFS traversal
        d = dict()       # Maps horizontal level to node value

        root.level = 0   # Root starts at level 0
        q.append(root)

        while len(q) != 0:
            root = q.pop(0)

            # If this level is not already recorded, add it
            if root.level not in d:
                d[root.level] = root.data

            # For left child: level is one less
            if root.left:
                root.left.level = root.level - 1
                q.append(root.left)

            # For right child: level is one more
            if root.right:
                root.right.level = root.level + 1
                q.append(root.right)

        # Print nodes from leftmost level to rightmost
        for i in sorted(d):
            print(d[i], end=' ')


# ----------- Main Execution -----------

if __name__ == "__main__":
    bt = BinarySearchTree()
    values = list(map(int, input("Enter values to insert into Binary Tree: ").split()))

    for val in values:
        bt.create(val)

    print("Top View of the Binary Tree:")
    bt.top_view(bt.root)

"""
============================
 Summary of Complexities
============================

Insertion:
    Average Time: O(log N)
    Worst Time: O(N)
    Space: O(1)

Top View:
    Time: O(N log N) [due to sorting the keys of horizontal levels]
    Space: O(N) [queue + dictionary]

Total Time: O(N log N)
Total Space: O(N)
"""