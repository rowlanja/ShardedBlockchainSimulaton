from node import Node

seed: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  192,
                        19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                        12, 62, 89, 110, 182, 9,   44, 20,  254, 22])

node1 = Node(seed, False, [14973], 14977, bytes([1, 2, 3, 4, 5]))

node1.listen()