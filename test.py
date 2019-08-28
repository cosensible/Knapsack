from queue import PriorityQueue
from collections import namedtuple

Node=namedtuple("Node",['est','cv','cld','ci','tk'])

q=PriorityQueue()
for i in range(5):
    q.put(Node(-i,i*2,i*3,i*4,i*5))

print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())

if q.empty():
    print("q is empty.")