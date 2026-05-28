import numpy as np
# a = np.array([1, 2, 3, 4, 5, 6])
# b = [1,2,3,4]
# print(a)
# print(b)
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [4,8,9],
              [5,8,9]])

b = a +5

print(b)
print(np.mean(a))

print(a.shape)
print(a.dtype)
print(a.ndim)
