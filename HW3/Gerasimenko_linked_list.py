class Node:
    # взято из семинара
    def __init__(self,data,next=None):
        self.data = data
        self.next = next


class LinkedList:
    # взято из семинара
    def __init__(self,head=None):
        self.head = head

    # взято из семинара
    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print() 

    # взято из семинара
    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    # взято из семинара
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node


    def size(self):
        listsize = 0
        node = self.head
        while node:
            listsize += 1
            node = node.next
        return listsize

    
    def insert(self,index,value):
        if index >= self.size():
            self.append(value)
        elif index == 0:
            self.push(value)
        else:
            findindex = 0
            node = self.head
            while node and findindex < index-1:
                findindex += 1
                node = node.next
            new_node = Node(value,node.next)
            node.next = new_node


    def delete(self,value):
        if self.head:
            if self.head.data == value:
                self.head = self.head.next
            else:
                prev = None
                node = self.head
                while node and node.data != value:
                    prev = node
                    node = node.next
                if node and node.data == value:
                    prev.next = node.next


    def reverse(self):
        curnode = self.head
        prev = None
        while curnode:
            nextnode = curnode.next
            curnode.next = prev
            prev = curnode
            curnode = nextnode
        self.head = prev     
