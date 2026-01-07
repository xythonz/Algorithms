def sort(unsorted):
    """Creates a binary tree from the list and performs an in-order traversal to sort it."""
    class TreeNode:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def insert(root, value):
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = insert(root.left, value)
        else:
            root.right = insert(root.right, value)
        return root

    def in_order_traversal(node, result):
        if node:
            in_order_traversal(node.left, result)
            result.append(node.value)
            in_order_traversal(node.right, result)

    root = None
    for value in unsorted:
        root = insert(root, value)

    sorted_list = []
    in_order_traversal(root, sorted_list)
    return sorted_list

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = "merge"