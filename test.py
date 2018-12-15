from functools import reduce



c = []

def f(x):
    return x * 2

for a in range(10):
    c.extend(f(a))


print(c)
#print(str(reduce(f,range(1, 999999))))