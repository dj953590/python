import numpy as np
my_list = [1,2,3]
print(np.array(my_list))
my_mat = [[1,2,3], [4,5,6]]
print(np.array(my_mat))
print(np.linspace(0,50,100))

np.random.rand(5)
np.random.randn(4,4)

arr_2d = np.arange(50).reshape(5,10)
print(arr_2d)
arr_2d = np.sqrt(arr_2d)
print(arr_2d)
arr_2d = np.log(arr_2d)
print(arr_2d)
