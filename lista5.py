from matplotlib import pyplot as plt
import imageio.v2 as imageio
from io import BytesIO
import random

class HashTable():
    def __init__(self, mod = 11):
        self._mod = mod
        self.pairs = [[] for _ in range(self._mod)]

    def insert_1(self, value):
        pos = (3*value + 5) % self._mod
        self.pairs[pos].append(value)
        self.__str__()

    def insert_2(self, value):
        pos = (3*value + 5) % self._mod
        while len(self.pairs[pos]) != 0:
            pos = (pos+1) % self._mod
        self.pairs[pos].append(value)
        self.__str__()

    def insert_3(self, value):
        pos = (3*value + 5) % self._mod
        f = 7 - (value % 7)
        it = 1
        n_pos = pos
        while len(self.pairs[n_pos]) != 0:
            n_pos = (pos+f*it) % self._mod
            it += 1
        self.pairs[n_pos].append(value)
        self.__str__()

    def __str__(self):
        print(self.pairs)

values = [12, 44, 13, 88, 23, 94, 11, 39, 20, 16, 5]

print('Zadanie 1')

def zad_1():
    h_table = HashTable()
    for i in values:
        h_table.insert_1(i)

zad_1()
print('Zadanie 2')

def zad_2():
    h_table = HashTable()
    for i in values:
        h_table.insert_2(i)

zad_2()
print('Zadanie 3')

def zad_3():
    h_table = HashTable()
    for i in values:
        h_table.insert_3(i)
zad_3()

def rearrange(array, start, end):
    j = start
    pivot = array[start]

    for i in range(start + 1, end):
        if array[i] < pivot:
            j += 1
            array[i], array[j] = array[j], array[i]

    array[start], array[j] = array[j], array[start] # pivot
    return j
            
def sort(array):
    stack = [(0, len(array))]
    gif = []
    while stack:
        start, end = stack.pop()
        if end - start > 1:
            gif.append(draw(array))
            index = rearrange(array, start, end)
            if index - start > end - index:
                stack.append((start, index))
                stack.append((index + 1, end))
            else:
                stack.append((index + 1, end))
                stack.append((start, index))
    imageio.mimsave('sortowanie.gif', gif, duration=0.5)
    return array

def draw(A):
    B = []
    for i in range(len(A)):
        B.append(i)
    
    plt.bar(B, A)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()

    buf.seek(0)
    img = imageio.imread(buf)
    return img

to_sort = []
for i in range(100):
    to_sort.append(random.randint(0, 200))

print(sort(to_sort))



