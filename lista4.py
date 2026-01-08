import time
import matplotlib.pyplot as plt
from graphviz import Digraph

class Node:
    def __init__(self, _value, _next = None):
        self.value = _value
        self.next = _next

class Stack(Node):
    def __init__(self, _value = None, _next = None):
        self.head = None
        self.length = 0
        if _value:
            self.push(_value)

    def extend(self, node):
        p = node
        while p:
            p = p.tail
            self.length += 1
        self.tail = node

    def __len__(self):
        return self.length
    
    def push(self, value):
        x = Node(value)
        x.head = self.head
        self.head = x
        self.length += 1
    
    def pop(self):
        if self.length == 0:
            raise IndexError('Can not pop an element')
        x = self.head.value
        self.head = self.head.head
        self.length -= 1
        return x
    
    def top(self):
        return self.head.value
    
    def __str__(self):
        p = self.head
        values = ''
        while p:
            values += str(p.value)
            values += ' '
            p = p.head
        return values

n = [(10000 // 10) * 10 * i for i in range(1, 11)]
pop_t = [0 for _ in range(10)]
push_t = [0 for _ in range(10)]
top_t = [0 for _ in range(10)]
rep = 10000

def measure(fun):
    t0 = time.perf_counter()
    fun()
    t1 = time.perf_counter()
    return t1 - t0

for _ in range(rep):
    for k in range(len(n)):
        size = n[k]
        stack = Stack()
        for _ in range(k):
            stack.push(1)
        push_t[k] += measure(lambda: stack.push(1))
        top_t[k] += measure(lambda: stack.top())
        pop_t[k] += measure(lambda: stack.pop())

for index in range(10):
    push_t[index] /= rep
    top_t[index] /= rep
    pop_t[index] /= rep
            

plt.plot(n, push_t, 'o')
plt.plot(n, top_t, 'o')
plt.plot(n, pop_t, 'o')
plt.title('push(), pop() and top() methods')
plt.xlabel('Number of elements')
plt.ylabel('Time needed')
plt.show()


## Zadanie 4

class BinaryTree():
    def __init__(self):
        self.tree = []

    def resize(self, new_size):
        x = len(self.tree)
        for _ in range(new_size - x):
            self.tree.append(None)

    def set_root(self, value):
        self.resize(1)
        self.tree[0] = value

    def set_left(self, parent_index, value):
        index = 2 *parent_index + 1
        self.resize(index + 1)
        self.tree[index] = value

    def set_right(self, parent_index, value):
        index = 2 *parent_index + 2
        self.resize(index + 1)
        self.tree[index] = value

    def get_left(self, parent_index):
        index = 2 * parent_index + 1
        if (len(self.tree) <= index):
            return None
        return self.tree[index]
    
    def get_right(self, parent_index):
        index = 2 * parent_index + 2
        if (len(self.tree) <= index):
            return None
        return self.tree[index]
    
    def get_parent(self, children_index):
        if len(self.tree) <= children_index:
            return False
        parent_index = (children_index - 1) // 2
        return self.tree[parent_index]
    
    def get_sibling(self, children_index):
        if children_index % 2 == 0:
            sibling_index = children_index - 1
        else:
            sibling_index = children_index + 1
        if sibling_index >= len(self.tree):
            return None
        return self.tree[sibling_index]
    
    def get_children(self, parent_index):
        return [self.get_left(parent_index), self.get_right(parent_index)]
    
    def get_root(self):
        if len(self.tree):
            return self.tree[0]
        else:
            return None
        
    def __getitem__(self, index):
        return self.tree[index]
    
    def draw(self, filename='tree'):
        tree = Digraph('Tree', format='png')
        self._draw_node(0, tree)
        tree.render(filename, cleanup=True)
    
    def __str__(self): 
        return str(self.tree)
    
    def _draw_node(self, index, t):
        if index >= len(self.tree) or self.tree[index] is None:
            return
        node_id = f'{index}'
        t.node(node_id, label=str(self.tree[index]))
        left_i = 2 * index + 1
        right_i = 2 * index + 2
        if self.get_left(index) is not None:
            t.node(f"{left_i}", label=str(self.tree[left_i]))
            t.edge(node_id, f"{left_i}", label="L")
            self._draw_node(left_i, t)

        if self.get_right(index) is not None:
            t.node(f"{right_i}", label=str(self.tree[right_i]))
            t.edge(node_id, f"{right_i}", label="R")
            self._draw_node(right_i, t)

def ex2():
    t = BinaryTree()
    t.set_root('/')
    t.set_left(0, '*')
    t.set_left(1,'+')
    t.set_right(1,'-')
    t.set_left(3, '5')
    t.set_right(3, '2')
    t.set_left(4,'2')
    t.set_right(4,'1')


    t.set_right(0, '*')
    t.set_left(2, '+')
    t.set_right(2, '8')
    t.set_left(5,'+')
    t.set_right(5,'-')
    t.set_left(11,'2')
    t.set_right(11, '9')
    t.set_right(12, '1')
    t.set_left(12, '-')
    t.set_right(25, '2')
    t.set_left(25, '7')
    t.draw('ex2')

def ex3():
    u = BinaryTree()
    u.set_root('E')
    u.set_left(0, 'X')
    u.set_right(0, 'N')
    u.set_left(1, 'A')
    u.set_right(1, 'U')
    u.set_left(3,'M')
    u.set_right(3,'F')
    u.draw('ex2')

ex3()

def derivative(bt, var):

    def read(i):
        if i >= len(bt.tree) or bt.tree[i] is None: 
            return None
        return (bt.tree[i], read(2*i+1), read(2*i+2))

    def Node(v, L=None, R=None): # wezel - wartosc + dwoje dzieci
        return (v, L, R)

    def d(t):
        if t is None: 
            return Node(0)
        v, L, R = t

        if isinstance(v, (int, float)): 
            return Node(0)

        if v == var:
            return Node(1)

        if v == "+": 
            return Node("+", d(L), d(R))
        if v == "-": 
            return Node("-", d(L), d(R))
        if v == "*": 
            return Node("+", Node("*", d(L), R), Node("*", L, d(R)))
        if v == "/":
            l = Node("-", Node("*", d(L), R), Node("*", L, d(R)))
            r = Node("^", R, Node(2))
            return Node("/", l, r)
        if v == "^":
            n = R[0]
            if n == 0:
                return Node(0)
            l = Node("*", Node(n), Node("^", L, Node(n-1)))
            return Node("*", l, d(L))
        if v == "sin": 
            return Node("*", Node("cos", L), d(L))
        if v == "cos": 
            return Node("-", Node(0), Node("*", Node("sin", L), d(L)))

    def write(t):
        out = BinaryTree()
        def go(node, i=0):
            if node is None: 
                return
            v, L, R = node
            out.resize(i+1)
            out.tree[i] = v
            go(L, 2*i+1)
            go(R, 2*i+2)
            
        go(t)
        return out

    new_tree = d(read(0))
    
    return write(new_tree)

bt = BinaryTree()
bt.set_root("+")
bt.set_left(0, "^")
bt.set_right(0, "*")

bt.set_left(1, "x")
bt.set_right(1, 3)

bt.set_left(2, 2)
bt.set_right(2, "x")

d_bt = derivative(bt, "x")
d_bt.draw()




