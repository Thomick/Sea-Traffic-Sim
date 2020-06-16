class Node_2L():
    def __init__(self, data, prev=None, nxt=None):
        self.data = data
        self.prev = prev
        self.nxt = nxt


class Queue():
    head = None
    tail = None
    length = 0
    max_length = -1

    def __init__(self, lst=[], max_length=-1):
        self.max_length = max_length
        if lst:
            for i in lst:
                self.append(i)

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.nxt

    def __repr__(self):
        return str(self.to_list())

    def __str__(self):
        return str(self.to_list())

    def __len__(self):
        return self.length

    def to_list(self):
        return [elt for elt in self]

    def append(self, elt):
        newNode = Node_2L(elt)
        if self.length == 0:
            self.head = newNode
            self.tail = newNode
        else:
            self.head.prev = newNode
            newNode.nxt = self.head
            self.head = newNode
        self.length += 1
        if self.length == self.max_length + 1:
            self.pop()

    def pop(self):
        elt = self.peek()
        if self.length > 1:
            self.tail.prev.nxt = None
            self.tail = self.tail.prev
            self.length -= 1
        else:
            self.head = None
            self.tail = None
            self.length = 0
        return elt

    def peek(self):
        elt = None
        if self.tail:
            elt = self.tail.data
        return elt
