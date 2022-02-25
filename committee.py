from node import Node
import logging
import threading
import time

seed: bytes = bytes([0,  50, 6,  244, 24,  199, 1,  25,  52,  88,  192,
                        19, 18, 12, 89,  6,   220, 18, 102, 58,  209, 82,
                        12, 62, 89, 110, 182, 9,   44, 20,  254, 22])

node1 = Node(seed, True, [14973,14974], 14977, bytes([1, 2, 3, 4, 5]))
node2 = Node(seed, False, [14974,14977], 14973, bytes([1, 2, 3, 4, 5]))
node3 = Node(seed, False, [14974,14977], 14973, bytes([1, 2, 3, 4, 5]))
node4 = Node(seed, False, [14974,14977], 14973, bytes([1, 2, 3, 4, 5]))


nodes = [node1,node2,node2,node3]

def thread_function(node):
    print("Thread starting")
    node.listen()
    print("Thread finishing")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(len(nodes)):
        node = nodes[index]
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(node,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)


