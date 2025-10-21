import os

def search_max(S, index=0, max=-10000000000):
    if index == len(S) - 1:
        return max
    if S[index] > max:
        max = S[index]
    # zlozonosc pamieci i miejca -> O(n)
    return search_max(S, index+1, max)

def power(x, n):
    """Compute the value x**n for integer n."""
    print(f'Wywolanie rekurencji dla pary {x, n} -> ')
    if n == 0:
        print(f'Otrzymana wartosc: {1}')
        return 1
    else:
        result = x*power(x, n-1)
        print(f'Otrzymana wartosc: {result}')
        return result

a = [1, 23, 4123,1111, 214123, 12312, 23123123, 123, 123, 231, 34]
print(search_max(a))

power(2, 5)

def min_max(S, index=0, min=100000, max=-100000):
    if len(S) - 1 == index:
        return [min, max]
    if S[index] > max:
        max = S[index]
    if S[index] < min:
        min = S[index]
    return min_max(S, index+1, min, max)

print(min_max(a))

# zadanie 4

def multiply(m, n):
    if n == 0:
        return 0
    elif n == 1:
        return m
    return m + multiply(m, n-1)

def check_palindrome(word, index = 0):
    n = len(word)
    if index + 1 > n / 2:
        return True
    if word[index] != word[n - index - 1]:
        return False 
    return check_palindrome(word, index+1)

print(check_palindrome('lkl'))

def find(path, filename):
    for name in os.listdir(path):
        full_name = os.path.join(path, name)
        if os.path.isfile(full_name) and name == filename:
            print(full_name)
        elif os.path.isdir(full_name):
            find(full_name, filename)


find('C:/Users/Kacper/Downloads/strona aktualna', 'sd.txt')