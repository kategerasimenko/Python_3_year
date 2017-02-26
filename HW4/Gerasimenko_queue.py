class Stack:
    def __init__(self): 
        self.stack = []


    def push(self, item): # положить элемент в стек
        self.stack.append(item)


    def pop(self): # удалить элемент из стека и вернуть его значение
        item = self.stack[-1]
        self.stack.pop()
        return item


    def peek(self): # вернуть значение последнего элемента стека (не удаляя его)
        item = self.stack[-1]
        return item


    def isEmpty(self): # вернуть True, если стек пуст, иначе вернуть False
        return not self.stack


class MyQueue:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()


    def enqueue(self, item): # положить элемент в очередь
        self.stack1.push(item)

    
    def dequeue(self): # удалить элемент из очереди и вернуть его значение
        if self.isEmpty():
            return 'nothing to delete'
        if self.stack2.isEmpty():
            while not self.stack1.isEmpty():
                item = self.stack1.pop()
                self.stack2.push(item)
        item = self.stack2.pop()
        return item


    def peek(self): # вернуть значение первого элемента очереди (не удаляя его)
        if self.isEmpty():
            return 'nothing to see'
        if self.stack2.isEmpty():
            while not self.stack1.isEmpty():
                item = self.stack1.pop()
                self.stack2.push(item)
        item = self.stack2.peek()
        return item


    def isEmpty(self): # вернуть True, если стек пуст, иначе вернуть False
        return self.stack1.isEmpty() and self.stack2.isEmpty()
    
