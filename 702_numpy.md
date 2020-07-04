### numpy

```python
import numpy as np
# 数组
a=np.array([1,2])
b=np.array([[1,2,3],
            [4,5,6]])
c=np.array([[[1,2,3],
            [4,5,6]],
          [[7,8,9],
          [10,11,12]]])

a=np.zeros(9) # 生成9个0的一维数组
a=np.ones((6,7)) # 生成6行7列全1二维数组
np.empty((2,4,5)) #生成三维数组

a=np.array([1,2,3],dtype=np.int32) #把元素全部转成int32类型（直接抹掉小数部分）
a=a.astype(np.float)#把元素全部转成float类型
a.dtype #获取a的元素类型

np.random.randn(4,3) #生成4行3列随机数数组

#矩阵
a=np.matrix([np.arange(5,9),np.arange(6,10)])

#运算
a=a*a  # 数组自乘，即aij=(aij)**2

array支持切片赋值a[1:3]=9，list则不行
对于二维数组，a[0:2]是前三行，a[0:2][0:2]是对于a[0:2]再取前三行，不是切列
a[0:2,0:2]是切前三行，前三列


布尔型索引：索引是一个命题
names=np.array(['jame','bob','kane','bob'])
num=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
print(num[names=='bob'])
[[ 4  5  6]
 [10 11 12]] # 即num对应names取第二行和第四行，因为这两行的names=='bob'的布尔值为True


转置 a=a.T
transpose()
reshape()
```

numpy文件存储

```python
a.tofile("a.bin")  # 转化为二进制文件
print(a.dtype)
b=np.fromfile("a.bin",dtype=...) # 必须设置b的类型为a的类型，否则结果是错的

np.save("a.npy",a)
b=np.load("a.npy")

np.savetxt('.csv/.txt',a,delimiter=',')  # 存进txt/csv，逗号分隔
b=np.loadtxt('.csv/.txt')
```

通用函数

```python
np.sqrt(a)
np.maximum(a,b)
```

numpy.where：依据条件批量处理元素

```python
arr=np.array([2,3,4,1])
arr=np.where(arr>2,2,arr) #np.where(条件，满足条件操作，不满足操作)
print(arr) #[2 2 2 1]
```

统计方法

```
arr=np.random.randn(2,4) #生成正态分布的二维数组，2行4列
print(arr)
print(arr.mean(axis=1)) #计算平均数，0：x轴（按行），1：y轴（按列）
print(arr.mean(axis=0))

arr.sum()
arr.cumsum()：求前缀和，返回一个数组
arr.argmin()最小项的索引
(np.abs(arr)>5).argmax()：第一个绝对值大于5的元素的索引

np.unique(array)去重

arr.sort()：排序
```

线性代数

```python
np.dot(arr1,arr2) #矩阵乘法

from numpy.linalg import inv,qr #线性代数模块
inv(arr) #求逆
q,r=qr(arr) #QR分解
svd(arr) #svd（奇异分解）

随机数seed
```

