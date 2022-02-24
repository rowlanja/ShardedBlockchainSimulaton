from .node import Node

seed: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  192,
                        19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                        12, 62, 89, 110, 182, 9,   44, 20,  254, 22])

node1 = Node(seed, True, [], 12345, bytes([1, 2, 3, 4, 5]))
node2 = Node(seed, False, [], 12346, bytes([1, 2, 3, 4, 5]))
node3 = Node(seed, False, [], 12347, bytes([1, 2, 3, 4, 5]))
node4 = Node(seed, False, [], 12348, bytes([1, 2, 3, 4, 5]))
node5 = Node(seed, False, [], 12349, bytes([1, 2, 3, 4, 5]))

node1.listen()
node2.listen()
node3.listen()
node4.listen()
node5.listen()