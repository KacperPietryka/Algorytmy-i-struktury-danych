from graphviz import Digraph
import random
import time
import matplotlib.pyplot as plt

class Node():
    def __init__(self, key = None, value = None, left = None, right = None):
        self.value = [key, value, 1]
        self.left = left
        self.right = right

class BinarySearchTree():
    def __init__(self, key = None, value = None):
        self.head = Node(key, value)
    
    def insert(self, key=0, value=None):
        if value == None:
            value = key

        if self.head.value == [None, None, 1]:
            self.head.value = [key, value, 1]
            return

        p = self.head

        node = Node(key, value)

        while p:
            if p.value[0] < key:
                if p.right is None:
                    p.right = node
                    return
                p = p.right
            elif p.value[0] > key:
                if p.left is None:
                    p.left = node
                    return
                p = p.left
            else:
                p.value[2] += 1
                return

    def search(self, x):
        if self.head.value[0] is None:
            return False
        p = self.head
        while p:
            if p.value[0] < x:
                p = p.right
            elif p.value[0] > x:
                p = p.left
            else:
                return p.value[2]
            
        return False
    
    def draw(self, filename='tree'):
        tree = Digraph('BST', format='png')
        self._draw_node(tree, self.head)
        tree.render(filename, cleanup=True)

    def _draw_node(self, t, node):
        node_id = str(id(node))
        t.node(node_id, label=f'{node.value[1]}   {node.value[2]}')

        if node.left:
            left_id = str(id(node.left))
            t.edge(node_id, left_id, label="L")
            self._draw_node(t, node.left)

        if node.right:
            right_id = str(id(node.right))
            t.edge(node_id, right_id, label="R")
            self._draw_node(t, node.right)

    def delete(self, key):
        if self.head.value[0] is None:
            return False

        p = self.head
        parent = None
        is_left = False

        while p and p.value[0] != key:
            parent = p
            if p.value[0] < key:
                is_left = False
                p = p.right
            else:
                is_left = True
                p = p.left

        if not p:
            return False

        if p.value[2] > 1:
            p.value[2] -= 1
            return p.value[2]

        if parent is None: # usuwamy korzeń
            if not (p.left or p.right):
                self.head.value = [None, None, 1]
                return True

            if p.right and not p.left:
                self.head = p.right
                return True

            if p.left and not p.right:
                self.head = p.left
                return True

            temp = p
            temp2 = p.left
            while temp2.right:
                temp = temp2
                temp2 = temp2.right

            p.value = temp2.value.copy()

            if temp is p:
                temp.left = temp2.left
            else:
                temp.right = temp2.left

            return True

        # nie usuwamy korzenia
        if not (p.left or p.right):
            if is_left:
                parent.left = None
            else:
                parent.right = None

        elif not p.left and p.right:
            child = p.right
            if is_left:
                parent.left = child
            else:
                parent.right = child

        elif not p.right and p.left:
            child = p.left
            if is_left:
                parent.left = child
            else:
                parent.right = child

        else:
            temp = p
            temp2 = p.left

            while temp2.right:
                temp = temp2
                temp2 = temp2.right

            p.value = temp2.value.copy()

            if temp is p:
                temp.left = temp2.left
            else:
                temp.right = temp2.left

        return True

# zadanie 2
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
    
    def draw(self, index = 0):
        tree = Digraph('Tree', format='png')
        self._draw_node(0, tree)
        fname = f'tree{index}'
        tree.render(fname, cleanup=True)
    
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

class HeapTree():
    def __init__(self):
        self.heaptree = BinaryTree()
        self.length = 0

    def heapify_up(self, ind):
        value = self.heaptree.tree[ind]
        while ind > 0:
            p = self.heaptree.get_parent(ind)
            parent = (ind - 1) // 2
            if p is None or p <= value:
                break
            self.heaptree.tree[ind] = p
            self.heaptree.tree[parent] = value
            ind = parent

    def heapify_down(self, ind):
        left = 2 * ind + 1
        right = 2 * ind + 2
        swap = ind

        if left < self.length and self.heaptree.tree[left] is not None:
            if self.heaptree.tree[left] < self.heaptree.tree[swap]:
                swap = left

        if right < self.length and self.heaptree.tree[right] is not None:
            if self.heaptree.tree[right] < self.heaptree.tree[swap]:
                swap = right

        if swap == ind:
            return

        self.heaptree.tree[ind], self.heaptree.tree[swap] = self.heaptree.tree[swap], self.heaptree.tree[ind]
        self.heapify_down(swap)

    def insert(self, value):
        index = self.length

        if index == 0:
            self.heaptree.set_root(value)
            self.length += 1
            return
        
        parent = (index - 1) // 2
        if index == 2 * parent + 1:
            self.heaptree.set_left(parent, value)
        else:
            self.heaptree.set_right(parent, value)
        
        self.heapify_up(index)
        self.length += 1
        return
    
    def delete(self, index = 0):
        ln = self.length
        if ln == 0 or ln <= index:
            return False
        del_val = self.heaptree.tree[index]
        self.heaptree.tree[index] = self.heaptree.tree[ln - 1]
        self.heaptree.tree[ln - 1] = None
        self.length -= 1

        if index == self.length:
            return del_val
        
        self.heapify_down(index)
        self.heapify_up(index)        
        return del_val

    def __str__(self):
        return str(self.heaptree)

class MinHeapTree(HeapTree):
    def __init__(self, limit = 10):
        self.limit = limit
        super().__init__()

    def insert(self, value):
        if self.limit > self.length:
            super().insert(value)
            return
        if value > self.heaptree.get_root():
            self.heaptree.tree[0] = value
            self.heapify_down(0)

def sort(unsorted_list):
    sorted = []
    ht = HeapTree()
    for i in unsorted_list:
        ht.insert(i)
    while ht.length > 0:
        sorted.append(ht.delete())
    return sorted

def measure_time():
    n = 1000
    t_counter = []
    n_list = []
    for i in range(0,50):
        n_list.append(n*(i+1)+10000)

    for i in range(0, 50):
        random_list = []
        for _ in range(n_list[i]):
            random_list.append(random.randint(0,10**5))
        t0 = time.perf_counter_ns()
        sort(random_list)
        t1 = time.perf_counter_ns()
        dt = t1 - t0
        t_counter.append(dt)
    
    filename = f"wykres.png"
    plt.plot(n_list, t_counter, 'o', markersize=5, label='wykres', color='green')
    plt.xlabel('n')
    plt.ylabel('Time (nanoseconds)')
    plt.legend()
    plt.title('Time complexity of following function')
    plt.grid()
    plt.savefig(filename)
    plt.close()

# zadanie 4 lista 5
l = [(1,'A'), (2, 'B'), (3,'C'), (4, 'D'), (5, 'E')]
bst = BinarySearchTree()
for i in range(len(l)):
    bst.insert(l[i][0], l[i][1])
    bst.draw(f'z4_bst{i}')

# zadanie 5 lista 5
bist = BinarySearchTree()
tab = [30, 40, 24, 58, 48, 26, 11, 13]
for i in range(len(tab)):
    bist.insert(tab[i])
    bist.draw(f'z5_bst{i}')

measure_time()

b = [1,2,3,344,12,2355,123,12]
print(sort(b))
