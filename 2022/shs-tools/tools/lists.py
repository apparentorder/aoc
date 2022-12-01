from dataclasses import dataclass
from typing import Any, Union


@dataclass
class Node:
    value: Any
    next: 'Node' = None
    prev: 'Node' = None


class LinkedList:
    _head: Union[Node, None] = None
    _tail: Union[Node, None] = None
    size: int = 0

    def _get_head(self):
        return self._head

    def _get_tail(self):
        return self._tail

    def _set_head(self, node: Node):
        node.next = self._head
        self._head.prev = node
        self._head = node

    def _set_tail(self, node: Node):
        node.prev = self._tail
        self._tail.next = node
        self._tail = node

    head = property(_get_head, _set_head)
    tail = property(_get_tail, _set_tail)

    def _append(self, obj: Any):
        node = Node(obj)
        if self._head is None:
            self._head = node

        if self._tail is None:
            self._tail = node
        else:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node

        self.size += 1

    def _insert(self, index: int, obj: Any):
        i_node = Node(obj)
        node = self._get_node(index)

        i_node.prev, i_node.next = node.prev, node
        node.prev = i_node
        if i_node.prev is not None:
            i_node.prev.next = i_node

        if index == 0:
            self._head = i_node

        self.size += 1

    def _get_node(self, index: int) -> Node:
        if index >= self.size or index < -self.size:
            raise IndexError("index out of bounds")

        if index < 0:
            index = self.size + index

        if index <= self.size // 2:
            x = 0
            node = self._head
            while x < index:
                x += 1
                node = node.next
        else:
            x = self.size - 1
            node = self._tail
            while x > index:
                x -= 1
                node = node.prev

        return node

    def _get(self, index: int) -> Any:
        return self._get_node(index).value

    def _pop(self, index: int = None) -> Any:
        if self.size == 0:
            raise IndexError("pop from empty list")

        if index is None:  # pop from the tail
            index = -1

        node = self._get_node(index)
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self._tail = node.prev

        ret = node.value
        del node
        self.size -= 1

        return ret

    def append(self, obj: Any):
        self._append(obj)

    def insert(self, index: int, obj: Any):
        self._insert(index, obj)

    def get(self, index: int) -> Any:
        return self._get(index)

    def pop(self, index: int = None) -> Any:
        return self._pop(index)

    def __contains__(self, obj: Any) -> bool:
        x = self._head
        while x.value != obj and x.next is not None:
            x = x.next

        return x.value == obj

    def __add__(self, other: 'LinkedList') -> 'LinkedList':
        self._tail.next = other.head
        other.head.prev = self._tail
        self._tail = other.tail
        self.size += other.size
        return self

    def __getitem__(self, index: int):
        return self._get(index)

    def __setitem__(self, index: int, obj: Any):
        self._get_node(index).value = obj

    def __len__(self):
        return self.size

    def __repr__(self):
        x = self._head
        if x is None:
            v = ""
        else:
            v = str(x.value)
            while x.next is not None:
                x = x.next
                v += ", " + str(x.value)
        return "%s(%s)" % (self.__class__.__name__, v)

    def __str__(self):
        return self.__repr__()


class Stack(LinkedList):
    def push(self, obj: Any):
        self._append(obj)

    def peek(self) -> Any:
        return self._tail.value


class Queue(LinkedList):
    def enqueue(self, obj: Any):
        self._append(obj)

    def dequeue(self) -> Any:
        return self._pop(0)

    def peek(self) -> Any:
        return self._head.value

    push = put = enqueue
    pop = get = dequeue
