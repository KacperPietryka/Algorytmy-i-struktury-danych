
import random
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.optimize import curve_fit

def eval_pow(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    return x * eval_pow(x, n-1)

def eval_pow_optimal(x, n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    if n % 2 == 0:
        return eval_pow_optimal(x*x, n/2)
    return x * eval_pow_optimal(x, n - 1)

def eval_polynomial(pol, n, x = 0):
    value = 0
    for i in range(0, n):
        value += pol[i] * eval_pow(x, i)
    # zlozonosc czasowa -> O(n^2) (dla kazdej potegi x^i mamy i operacji (plus mnozenie * a[i] i dodanie, czyli mamy 
    # i + 2 lacznie), suma to bedzie (n+4)n/2
    # zlozonosc pamieciowa ->  o(n) - przez rekurencje
    return value

def eval_polynomial_2(pol, n, x = 0):
    value = 0
    for i in range(0, n):
        value += pol[i] * eval_pow_optimal(x, i)
    # zlozonosc czasowa -> O(n log n) (dla kazdej potegi x^i mamy [log(i)] [zaokraglenie w gore] operacji
    # suma to bedzie n(log [(n + 2)] + log [3])/2
    # zlozonosc pamieciowa ->  O(log n)
    return value

def Horner(pol, n, x=0):
    value = 0
    for i in range(n - 1, 0, -1):
        value = (value + pol[i]) * x
    value += pol[0]
    # zlozonosc czasowa: 0(n), zlozonosc pamieciowa: 0(1) 
    return value

print(eval_polynomial([2, 1, 3], 3, 4))
print(eval_polynomial_2([2, 1, 3], 3, 4))
print(Horner([2, 1, 3], 3, 4))

# Zadanie 2

def example1(S):
    """Return the sum of the elements in sequence S."""
    n = len(S)
    total = 0
    for j in range(n):
        total += S[j]
    return total
def example2(S):
    """Return the sum of the elements with even index in sequence S.
    """
    n = len(S)
    total = 0
    for j in range(0, n, 2):
        total += S[j]
    return total
def example3(S):
    """Return the sum of the prex sums of sequence S."""
    n = len(S)
    total = 0
    for j in range(n):
        for k in range(1+j):
            total += S[k]
    return total

def example4(A, B): # assume that A and B have equal length
    """Return the number of elements in B equal to the sum of prex
    sums in A."""
    n = len(A)
    count = 0
    for i in range(n):
        total = 0
        for j in range(n):
            for k in range(1+j):
                total += A[k]
            if B[i] == total:
                count += 1
    return count


list_1 = [1000, 5000]
list_2 = [10000, 50000]
list_3 = [10, 200]
list_4 = [10, 200] 
list_n = [list_1,list_2,list_3,list_4]
time_ = [[],[],[],[]]
functions = [example1, example2, example3, example4]

def plot_times(x,y, title='Function'):
    filename = f"{title}.png"
    plt.plot(x, y, 'o', markersize=5, label=title, color='green')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Time complexity of following function')
    plt.grid()
    plt.savefig(filename)
    plt.close()

def ex_2():
    for fun_index in range(4):
        results = []
        for n in range(100): # 100 losowych wartosci z tego przedzialu 
            seq = []
            seq_2 = []
            result = random.randint(list_n[fun_index][0], list_n[fun_index][1])
            results.append(result)
            for i in range(result):
                a = random.randint(0, 10)
                b = random.randint(0, 10)
                seq_2.append(b)
                seq.append(a)
            start = time.perf_counter()
            if fun_index == 3:
                functions[fun_index](seq, seq_2)
            else:
                functions[fun_index](seq)
            end = time.perf_counter()
            time_[fun_index].append(end - start)
        plot_times(results, time_[fun_index], title=f'Function {fun_index+1}')
        #print('Koniec')

ex_2()

# SORTED function
seq = []
time_sorted = []
n_sorted = sorted(random.sample(range(1000, 10000), 200))
for n in n_sorted:
    seq = []
    for i in range(n):
        a = random.randint(0, 10)
        seq.append(a)
    start = time.perf_counter()
    sorted(seq)
    end = time.perf_counter()
    time_sorted.append(end - start)

def model(n, a, b):
    return a * n * np.log2(n) + b

n_sorted = np.array(n_sorted)
time_sorted = np.array(time_sorted)
params, _ = curve_fit(model, n_sorted, time_sorted)
a, b = params
f = model(n_sorted, a, b)

print(a, b)

n_points = np.linspace(n_sorted[0], n_sorted[199], 200)
label = f'{a:.1e}*nlog + {b:.1e}'
plt.plot(n_sorted, time_sorted, 'o', linewidth=1, label='Function sorted()')
plt.plot(n_points, f, markersize=1, linewidth=4, label=label)

plt.xlabel('n')
plt.ylabel('Time (seconds)')
plt.legend()
plt.title('Time complexity of following function')
plt.grid()
plt.savefig('Sorted.png')
plt.close()