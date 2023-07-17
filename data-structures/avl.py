# Name: Riley Ovenshire
# OSU Email: ovenshir@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Binary Search Tree Implementation
# Due Date: May 23, 2023 (used a free day)
# Description: Implement BST class and its methods, then use those methods in an AVL tree.

import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree, maintaining AVL tree properties. Duplicate values should be ignored. O(log(n))

        Receives: value to add
        Returns: nothing
        """
        # Exploration AVL Implementation / Module 6
        # SOURCE: https://www.youtube.com/watch?v=8ZFKANrvp7E&ab_channel=TreesStack
        # SOURCE: https://www.youtube.com/watch?v=jDM6_TnYIqE&t=1972s&ab_channel=AbdulBari

        # I've tried really, really hard to get this to work and I just cannot seem to figure out what is wrong.
        # At this point I'm just going to submit what I have and hope for the best.
        # Any feedback on what I'm doing wrong would be greatly appreciated.

        added_node = AVLNode(value)
        if self._root is None:
            self._root = added_node
            return
        parent = self.find_node_parent(value)
        if parent is None:
            return
        if parent.value > value:
            parent.left = added_node
        else:
            parent.right = added_node
        added_node.parent = parent
        self._update_height(added_node)
        self._rebalance(added_node)

    def find_node(self, value: object) -> AVLNode:
        """
        Finds the node with the given value. O(log(n))

        Receives: value to find
        Returns: node with given value
        """
        if self._root is None:
            return None

        current = self._root
        while current is not None:
            if current.value == value:
                return current
            elif current.value > value:
                current = current.left
            else:
                current = current.right
        return None

    def find_node_parent(self, value: object):
        """
        Finds the parent of the node with the given value. O(log(n))

        Receives: value to find
        Returns: parent of node with given value
        """
        if self._root is None:
            return None

        current = self._root
        while current is not None:
            if current.value == value:
                return current.parent
            elif current.value > value:
                current = current.left
            else:
                current = current.right
        return None

    def remove(self, value: object) -> bool:
        """
        Removes the node with the given value from the tree, maintaining AVL tree properties. O(log(n))

        Receives: value to remove
        Returns: True if value was removed, False if value not found
        """

        # I've tried really, really hard to get this to work and I just cannot seem to figure out what is wrong.
        # At this point I'm just going to submit what I have and hope for the best.
        # Any feedback on what I'm doing wrong would be greatly appreciated.

        if self._root is None:
            return False
        node = self.find_node(value)
        if node is None:
            return False
        if node.left is None and node.right is None:
            self._remove_leaf(node)
        elif node.left is None or node.right is None:
            self._remove_one_subtree(node)
        else:
            self._remove_two_subtrees(node)
        self._rebalance(node.parent)
        return True

    def _remove_leaf(self, node: AVLNode) -> None:
        """
        Removes a leaf node from the tree. O(1)

        Receives: node to remove
        Returns: nothing
        """
        if node.parent is None:
            self._root = None
        elif node.parent.left == node:
            node.parent.left = None
        else:
            node.parent.right = None

    def _remove_one_subtree(self, node: AVLNode) -> None:
        """
        Removes a node with one child from the tree. O(1)

        Receives: node to remove
        Returns: nothing
        """
        if node.parent is None:
            if node.left is not None:
                self._root = node.left
            else:
                self._root = node.right
        elif node.parent.left == node:
            if node.left is not None:
                node.parent.left = node.left
            else:
                node.parent.left = node.right
        else:
            if node.left is not None:
                node.parent.right = node.left
            else:
                node.parent.right = node.right

    def _remove_two_subtrees(self, node: AVLNode) -> None:
        """
        Removes a node with two children from the tree. O(log(n))

        Receives: node to remove
        Returns: nothing
        """
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        self._remove_leaf(successor)


    def _balance_factor(self, node: AVLNode) -> int:
        """
        Finds the balance factor of a node. O(1)

        Receives: node to find balance factor of
        Returns: balance factor of node
        """
        if node is None:
            return 0
        left = self._get_height(node.left)
        right = self._get_height(node.right)
        return left - right

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of the given node. O(1)

        Receives: node to find height of
        Returns: height of node
        """
        if node is None:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Left rotation for given node. O(1).

        Receives: node to rotate
        Returns: new root of subtree
        """
        # Exploration - Rotation Implementation
        # SOURCE: https://www.youtube.com/watch?v=jDM6_TnYIqE&t=1972s&ab_channel=AbdulBari

        new_root = node.right
        node.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self._root = new_root
        elif node is node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root
        new_root.left = node
        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Right rotation for given node. O(1).

        Receives: node to rotate
        Returns: new root of subtree
        """
        # Exploration - Rotation Implementation
        # SOURCE: https://www.youtube.com/watch?v=jDM6_TnYIqE&t=1972s&ab_channel=AbdulBari

        new_root = node.left
        node.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = node
        new_root.parent = node.parent
        if node.parent is None:
            self._root = new_root
        elif node is node.parent.right:
            node.parent.right = new_root
        else:
            node.parent.left = new_root
        new_root.right = node
        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the given node. O(1)

        Receives: node to update height of
        Returns: nothing
        """
        # Exploration AVL Implementation / Module 6
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1


    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances the tree after any manipulation to the tree. O(1)

        receives: node to rebalance
        Returns: nothing
        """
        # Exploration - Rotation Implementation
        # SOURCE: https://www.youtube.com/watch?v=jDM6_TnYIqE&t=1972s&ab_channel=AbdulBari

        bf = self._balance_factor(node)

        if bf < -1:         # right heavy
            if self._balance_factor(node.left) > 0: # do we need a double rotation?
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            new_root = self._rotate_right(node)
            new_root.parent = node.parent          # whenever a node is rotated, its parent changes
            node.parent.left = new_root
        elif bf > 1:        # left heavy
            if self._balance_factor(node.right) < 0: # do we need a double rotation?
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            new_root = self._rotate_left(node)
            new_root.parent = node.parent
            node.parent.right = new_root
        else:                                       # still need to update height
            self._update_height(node)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),  # RR, RR
        (10, 20, 30, 50, 40),  # RR, RL
        (30, 20, 10, 5, 1),  # LL, LL
        (30, 20, 10, 1, 5),  # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
