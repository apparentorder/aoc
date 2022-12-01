from heapq import heappop, heappush
from tools.trees import MinHeap, BinarySearchTree
from tools.stopwatch import StopWatch


s = StopWatch()
h = []
for x in range(100_000):
    heappush(h, x)
print("Heappush:", s.elapsed())
s.reset()
while h:
    heappop(h)
print("Heappop:", s.elapsed())

s = StopWatch()
h = MinHeap()
for x in range(100_000):
    h.add(x)
print("MinHeap.add():", s.elapsed())
s.reset()
while not h.empty():
    h.pop()
print("MinHeap.pop():", s.elapsed())

s = StopWatch()
b = set()
for x in range(1_000_000):
    b.add(x)
print("set.add():", s.elapsed())
s.reset()
for x in range(1_000_000):
    _ = x in b
print("x in set:", s.elapsed())

s = StopWatch()
b = BinarySearchTree()
for x in range(1_000_000):
    b.add(x)
print("AVL.add():", s.elapsed())
s.reset()
for x in range(1_000_000):
    _ = x in b
print("x in AVL:", s.elapsed())

print("DFS/BFS Test")
b = BinarySearchTree()
for x in range(20):
    b.add(x)
b.print()
print("DFS:")
for x in b.iter_depth_first():
    print(x)
print("BFS:")
for x in b.iter_breadth_first():
    print(x)
