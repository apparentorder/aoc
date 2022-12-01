from dataclasses import dataclass, field
from enum import Enum
from tools.lists import Queue, Stack
from typing import Any, List, Union


class Rotate(Enum):
    LEFT = 0
    RIGHT = 1


@dataclass
class TreeNode:
    value: Any
    parent: Union['TreeNode', None] = None
    left: Union['TreeNode', None] = None
    right: Union['TreeNode', None] = None
    balance_factor: int = 0
    height: int = 0

    def __str__(self):
        return "TreeNode:(%s; bf: %d, d: %d, p: %s, l: %s, r: %s)" \
            % (self.value, self.balance_factor, self.height,
               self.parent.value if self.parent else "None",
               self.left.value if self.left else "None",
               self.right.value if self.right else "None")

    def __repr__(self):
        return str(self)


class TrieNode:
    value: str
    parent: Union['TrieNode', None] = None
    children: List['TrieNode'] = field(default_factory=list)


def update_node(node: TreeNode):
    left_depth = node.left.height if node.left is not None else -1
    right_depth = node.right.height if node.right is not None else -1
    node.height = 1 + (left_depth if left_depth > right_depth else right_depth)
    node.balance_factor = right_depth - left_depth


class BinaryTree:
    root: Union[TreeNode, None] = None
    node_count: int = 0

    def _insert(self, node: TreeNode, parent: TreeNode, obj: Any) -> TreeNode:
        new_node = TreeNode(obj, parent)
        if node is None:
            return new_node

        found = False
        while not found:
            if obj < node.value:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = new_node
                    found = True
            elif obj > node.value:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = new_node
                    found = True
            else:
                raise ValueError("obj already present in tree: %s" % obj)

        new_node.parent = node
        return new_node

    def _remove(self, node: TreeNode):
        if node.left is None and node.right is None:  # leaf node
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                self.root = None
        elif node.left is not None and node.right is not None:  # both subtrees present
            d_node = node.left
            while d_node.right is not None:
                d_node = d_node.right
            node.value = d_node.value
            self.remove(node.value, d_node)
        elif node.left is None:  # only a subtree on the right
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
            else:
                self.root = node.right
            node.right.parent = node.parent
        else:  # only a subtree on the left
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
            else:
                self.root = node.left
            node.left.parent = node.parent

        self.node_count -= 1

    def _get_node_by_value(self, obj: Any, root_node: TreeNode = None) -> TreeNode:
        if self.root is None:
            raise IndexError("get node from empty tree")

        if root_node is None:
            root_node = self.root

        node = root_node
        while node is not None:
            if obj < node.value:
                node = node.left
            elif obj > node.value:
                node = node.right
            else:
                return node

        raise ValueError("obj not in tree:", obj)

    def add(self, obj: Any):
        if obj is None:
            return

        new_node = self._insert(self.root, self.root, obj)
        if self.root is None:
            self.root = new_node
        self.node_count += 1

    def remove(self, obj: Any, root_node: TreeNode = None):
        node = self._get_node_by_value(obj, root_node)
        self._remove(node)

    def iter_depth_first(self):
        stack = Stack()
        stack.push(self.root)
        while len(stack):
            node = stack.pop()
            if node.right is not None:
                stack.push(node.right)
            if node.left is not None:
                stack.push(node.left)
            yield node.value

    def iter_breadth_first(self):
        queue = Queue()
        queue.push(self.root)
        while len(queue):
            node = queue.pop()
            if node.left is not None:
                queue.push(node.left)
            if node.right is not None:
                queue.push(node.right)
            yield node.value

    def print(self, node: TreeNode = None, level: int = 0):
        if node is None:
            if level == 0 and self.root is not None:
                node = self.root
            else:
                return

        self.print(node.right, level + 1)
        print(" " * 4 * level + '->', node)
        self.print(node.left, level + 1)

    def __contains__(self, obj: Any) -> bool:
        if self.root is None:
            return False

        c_node = self.root
        while c_node is not None:
            if obj == c_node.value:
                return True
            elif obj < c_node.value:
                c_node = c_node.left
            else:
                c_node = c_node.right

        return False

    def __len__(self) -> int:
        return self.node_count


class BinarySearchTree(BinaryTree):
    def _balance(self, node: TreeNode) -> TreeNode:
        if node.balance_factor == -2:
            if node.left.balance_factor <= 0:
                return self.rotate(Rotate.RIGHT, node)
            else:
                return self.rotate(Rotate.RIGHT, self.rotate(Rotate.LEFT, node.left))
        elif node.balance_factor == 2:
            if node.right.balance_factor >= 0:
                return self.rotate(Rotate.LEFT, node)
            else:
                return self.rotate(Rotate.LEFT, self.rotate(Rotate.RIGHT, node.right))
        else:
            return node

    def _insert(self, node: TreeNode, parent: TreeNode, obj: Any) -> TreeNode:
        node = super()._insert(node, parent, obj)
        if self.root is not None:
            while node is not None:
                update_node(node)
                node = self._balance(node).parent
        return node

    def remove(self, obj: Any, root_node: TreeNode = None):
        if root_node is None:
            root_node = self.root

        super().remove(obj, root_node)
        update_node(root_node)
        self._balance(root_node)

    def rotate(self, direction: Rotate, node: TreeNode = None) -> TreeNode:
        if node is None:
            node = self.root

        parent = node.parent
        if direction == Rotate.LEFT:
            pivot = node.right
            node.right = pivot.left
            if pivot.left is not None:
                pivot.left.parent = node
            pivot.left = node
        else:
            pivot = node.left
            node.left = pivot.right
            if pivot.right is not None:
                pivot.right.parent = node
            pivot.right = node

        node.parent = pivot
        pivot.parent = parent

        if parent is not None:
            if parent.left == node:
                parent.left = pivot
            else:
                parent.right = pivot

        if node == self.root:
            self.root = pivot

        update_node(node)
        update_node(pivot)

        return pivot


class Heap(BinarySearchTree):
    def empty(self):
        return self.root is None

    def popMin(self):
        if self.root is None:
            raise IndexError("pop from empty heap")

        c_node = self.root
        while c_node.left is not None:
            c_node = c_node.left

        ret = c_node.value
        self._remove(c_node)
        return ret

    def popMax(self):
        if self.root is None:
            raise IndexError("pop from empty heap")

        c_node = self.root
        while c_node.right is not None:
            c_node = c_node.right

        ret = c_node.value
        self._remove(c_node)
        return ret


class MinHeap(Heap):
    def pop(self):
        return self.popMin()


class MaxHeap(Heap):
    def pop(self):
        return self.popMax()
