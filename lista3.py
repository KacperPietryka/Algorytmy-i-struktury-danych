
import ctypes
import random
import time
import matplotlib.pyplot as plt

class DynamicArray:
    def __init__(self):
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    def insert(self, k, value):
        if self._capacity == self._n:
            self._resize(2*self._capacity)
        if k >= self._n:
            self._A[self._n] = value
            self._n += 1
            return
        for i in range(self._n - 1, k-1, -1):
            self._A[i+1] = self._A[i]
        self._A[k] = value
        self._n += 1

    def remove(self, value):
        for i in range(self._n):
            if value == self._A[i]:
                for k in range(i, self._n - 1):
                    self._A[k] = self._A[k + 1]
                self._n -= 1
                return i

    def expand(self, seq):
        new_length = self._n + len(seq)
        if(self._capacity <= new_length):
            self._resize(new_length)
        for i in range(len(seq)):
            self._A[self._n + i] = seq[i]
        self._n = new_length

    def __str__(self):
        result = ''
        for i in range(self._n):
            result += str(self._A[i])
            result += ' '
        return result

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]

    def append(self, obj):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    def _make_array(self, c):
        return (c*ctypes.py_object)()

arr = DynamicArray()
arr.append(1)
arr.append(2)
arr.append(3)
arr.insert(1,2)
arr.remove(12)
arr.expand([1,23,32])
print(arr)

# zadanie 2
len_ = 1000000
lst = list(range(len_))

for i in range(len_):
    lst.append(random.randint(1,10))

T = []
n = 20
deletion = [i * (len_ // n) for i in range(n)]

for i in range(n):
    sum = 0
    for k in range(100):
        start = time.perf_counter()
        lst.pop(deletion[i])
        end = time.perf_counter()
        sum += end - start
        lst.append(0)
    T.append(sum / 100) # average time

plt.figure()
plt.title('Deletion time (on the same list) at a given index')
plt.xlabel('Number of elements')
plt.ylabel('Time needed')
labels = [f"A[{i}/n]" for i in range(n)] 
x = list(range(len(deletion)))
plt.bar(x, T)
plt.xticks(range(len(deletion)), labels)
plt.show()

def sum(array):
    sum = 0
    n = len(array)
    for i in range(n):
        for k in range(n):
            sum += array[i][k]
    return sum

print(sum([[1,3],[2,4]]))


# Zadanie 4
sizes = [i * (100000 // 100) for i in range(100)]
case_1 = [] # time1
case_2 = [] # time2

def t_calc(t0):
    t1 = time.perf_counter()
    delta_t = t1 - t0
    return delta_t

for i in range(len(sizes)):
    new_array = []
    t0 = time.perf_counter()
    for k in range(sizes[i]):
        new_array.append(1)
    case_1.append(t_calc(t0))

    new_array_2 = []
    t0 = time.perf_counter()
    new_array_2.extend(new_array)
    case_2.append(t_calc(t0))

plt.plot(sizes, case_1, 'o')
plt.plot(sizes, case_2, 'o')
plt.title('Append (blue) vs Extend funtion(orange)')
plt.xlabel('Number of elements')
plt.ylabel('Time needed')
plt.grid()
plt.show()

class Empty(Exception):
    pass
    
class Queue:
    DEFAULT_CAPACITY = 10

    def __init__(self):
        self._data = [None] * Queue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]
    
    # my function for memory release
    def memory_release(self):
        if 2*self._size + 8 < len(self._data):
            self._resize(self._size + 8)

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        value = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        self.memory_release()
        return value

    def enqueue(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0

class DoubleQueue(Queue):
    def add_last(self, x):
        super().enqueue(x)
    def delete_first(self):
        return super().dequeue()
    
    # first(), is_empty() and __len__() methods are defined in main class

    def delete_last(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        _back = (self._front + self._size - 1) % len(self._data)
        value = self._data[_back]
        self._data[_back] = None
        self._size -= 1
        self.memory_release()
        return value
    
    def last(self):
        if self.is_empty():
            raise Empty('Deque is empty!')
        _back = (self._front + self._size - 1) % len(self._data)
        return self._data[_back]
    
    def add_first(self, x):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = x
        self._size += 1

# zadanie 7
class Stack:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)
    
    def is_empty(self):
        return len(self._data)==0
    
    def push(self,e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]
    
    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()


def repeated(brackets_open, brackets_close, string):
    lst = Stack()
    for i in string:
        if i in brackets_open:
            lst.push(i)
        for index in range(len(brackets_close)):
            if i == brackets_close[index]:
                if lst.is_empty():
                    return False
                bracket = lst.pop()
                if brackets_open[index] != bracket:
                    return False
    if not lst.is_empty():
        return False
    return True

b_open = ['(','{','<', '[']
b_closed = [')', '}', '>', ']']

print(repeated(b_open, b_closed, '<html><head><title>T</title></head><body><div><p>OK</p></div></body></html>'))

# zadanie 8

def permutations(n):
    stack_1 = Stack()
    stack_1.push(([], list(range(1, n + 1))))

    while not stack_1.is_empty():
        prefix, remain = stack_1.pop()

        if not remain:
            print(prefix)
            continue

        for i, x in enumerate(remain):
            new_prefix = prefix + [x]
            new_remain = remain[:i] + remain[i+1:]
            stack_1.push((new_prefix, new_remain))

permutations(3)


class Stack_Queue():
    def __init__(self):
        self.q = Queue()

    def __len__(self):
        return len(self.q)

    def is_empty(self):
        return self.q.is_empty()

    def pop(self):
        if self.is_empty():
            raise Empty('Empty Stack')
        return self.q.dequeue()

    def push(self, x):
        self.q.enqueue(x)
        for _ in range(len(self.q) - 1):
            self.q.enqueue(self.q.dequeue()) # A B C -> (+D) -> A B C D -> B C D A -> ... -> D A B C   

    def top(self):
        if self.q.is_empty():
            raise Empty('Queue is empty')
        return self.q.first()

class Queue_stack():
    def __init__(self):
        self.s1 = Stack()
        self.s2 = Stack()
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.s1.is_empty()

    def enqueue(self, x):
        self.s1.push(x)
        self.size += 1

    def dequeue(self):
        if self.s1.is_empty():
            raise Empty('Empty Queue')
        for _ in range(self.size - 1):
            self.s2.push(self.s1.pop())
        x = self.s1.pop()
        self.size -= 1
        for _ in range(self.size):
            self.s1.push(self.s2.pop())
        return x
    
    def first(self):
        if self.s1.is_empty():
            raise Empty('Empty Queue')
        for _ in range(self.size):
            self.s2.push(self.s1.pop())
        x = self.s2.top()
        for _ in range(self.size):
            self.s1.push(self.s2.pop())            
        return x