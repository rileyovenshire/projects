# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Binary Search Tree Implementation
# Due Date: May 23, 2023 (used a free day)
# Description: Implement BST class and its methods, then use those methods in an AVL tree.

import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #


    # Emailed Dr. Chaundhry about using a free day - decided to start the assignment over again. See past submissions for previous work.


    def add(self, value: object) -> None:
        """
        Adds a value to the tree. Duplicates are allowed. If node with value is already in tree, new value should be added to the right subtree.

        Receives: value to add
        Returns: nothing
        """
        parent = None
        current = self._root

        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if parent is None:
            self._root = BSTNode(value)
        elif value < parent.value:
            parent.left = BSTNode(value)
        else:
            parent.right = BSTNode(value)


    def remove(self, value: object) -> bool:
        """
        Remove a value from the tree. Return true if removed, false if not found.

        Receives: value to remove
        Returns: True if value was removed, False if not found
        """
        # Exploration BST Operations for reference
        # SOURCES CITED:
        #   https://www.youtube.com/watch?v=wMyWHO9F1OM&ab_channel=TimothyHChang , implemented with O(h) but
        #       I used the site below for O(n) implementation
        #   https://www.geeksforgeeks.org/inorder-predecessor-successor-given-key-bst/
        #   with this video: https://www.youtube.com/watch?v=1FSDhZRZ7bw&ab_channel=GeeksforGeeks

        # if tree is empty, return False
        if self._root is None:
            return False

        # first, search for node to remove (Timothy Chang's video, step 1)
        def find_node(node, value):
            if node is None:
                return None
            elif node.value == value:
                return node
            elif value < node.value:
                return find_node(node.left, value)
            else:
                return find_node(node.right, value)

        # next, find the inorder successor (Timothy Chang's video, step 2)
        def find_inorder_successor(node):
            current = node.right
            while current.left is not None:
                current = current.left
            return current

        # finally, remove the node (Timothy Chang's video, step 3)
        def remove_node(node, value):
            if node is None:
                return None
            elif value < node.value:
                node.left = remove_node(node.left, value)
            elif value > node.value:
                node.right = remove_node(node.right, value)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    successor = find_inorder_successor(node)
                    node.value = successor.value
                    node.right = remove_node(node.right, successor.value)

            return node

        # call above functions, complete the problem
        target = find_node(self._root, value)
        if target is None:
            return False

        else:
            self._root = remove_node(self._root, value)
            return True


    def find_node_and_parent(self, value: object) -> (BSTNode, BSTNode):
        """
        Finds a node with the given value and its parent node. Returns None if not found.

        Receives: value to find
        Returns: node with given value and its parent node
        """
        # find the node to remove and its parent, psuedocode from Exploration
        parent = None
        current = self._root

        while current is not None:
            if value == current.value:
                return current, parent
            elif value < current.value:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right
        return None, None

    def find_inorder_successor(self, node: BSTNode) -> BSTNode:
        """
        Finds the inorder successor of a node.

        Receives: node to find inorder successor of
        Returns: inorder successor of node
        """
        current = node.right
        while current.left is not None:
            current = current.left
        return current


    def find_inorder_successor_parent(self, node: BSTNode) -> BSTNode:
        """
        Finds the parent of the inorder successor of a node.

        Receives: node to find inorder successor of
        Returns: parent of inorder successor of node
        """
        parent = node
        current = node.right
        while current.left is not None:
            parent = current
            current = current.left
        return parent

    def contains(self, value: object) -> bool:
        """
        Returns true if value is in the tree, false if not.

        Receives: value to search for
        Returns: True if value is in the tree, False if not
        """
        current = self._root
        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def inorder_traversal(self) -> Queue:
        """
        Performs inorder traversal of the tree, returns Queue object that has visited nodes in order. Empty tree returns empty Queue.

        Receives: nothing
        Returns: Queue object with visited nodes in order
        """
        queue = Queue()
        self.inorder_traversal_helper(self._root, queue)
        return queue

    def inorder_traversal_helper(self, node: BSTNode, queue: Queue) -> None:
        """
        Recursive helper for inorder traversal.

        Receives: node to start at, queue to add to
        Returns: nothing
        """
        if node is not None:
            self.inorder_traversal_helper(node.left, queue)
            queue.enqueue(node.value)
            self.inorder_traversal_helper(node.right, queue)

    def find_min(self) -> object:
        """
        Finds the minimum value in the tree.

        Receives: nothing
        Returns: minimum value in the tree
        """
        if self._root is None:
            return None
        current = self._root
        while current.left is not None:
            current = current.left
        return current.value

    def find_max(self) -> object:
        """
        Finds the maximum value in the tree.

        Receives: nothing
        Returns: maximum value in the tree
        """
        if self._root is None:
            return None
        current = self._root
        while current.right is not None:
            current = current.right
        return current.value

    def is_empty(self) -> bool:
        """
        Returns True if tree is empty, False if not.

        Receives: nothing
        Returns: True if tree is empty, False if not
        """
        if self._root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        Remove all nodes

        Receives: nothing
        Returns: nothing
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
