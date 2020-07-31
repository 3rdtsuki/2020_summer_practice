```python
pip install ... -i https://mirrors.aliyun.com/pypi/simple
pip install ... -i https://pypi.tuna.tsinghua.edu.cn/simple

%d,%s
print('%d*%d=%d'%(a,b,c))
print('{0}*{1}={2}'.format(a,b,c)) #格式化输出

str.count('i')：计数
str.index：找不到报错
str.find('i')：找不到return -1
str.replace('n','k')
str.split()
str.strip()移除头尾空格

元组tuple = (1, 2, 3, 4, 5),只读
列表list=[1, 2, 3, 4, 5],list.sort()
字典dic={key1:value1,key2:value2}
集合set={1,2.3}，集合是无序的，没有键值对，set1=set()，创建，不然视为字典，主要用来去重

多个随机数：
random.randint(0,100,size=9)

#iterator迭代器
listiter=iter(menu)
while True:
    try:
        print(next(listiter))
    except StopIteration:
        break
        
推导式：
l=[i*3.1415 for i in range(0,100) if i%2==0]
字典推导式：
l={'a':10,'b':11,'A':21}
freq={
    k.lower():l.get(k.lower(),0)+l.get(k.upper(),0) #dict.get(a,0):元素a不在dict中返回0
    for k in l.keys()
    if k.lower() in ['a','b']
}
print(freq)

```

异常

```
try:...except ValueError:...
ex=Exception("error")
raise ex

try:
    a
except NameError as aaa:
    print(aaa) #打印具体异常信息

```

函数

```python
def f(a,b,c=200):#默认参数必须在最后
    print(a,b,c)
f(2,3,4) #默认c=200，但如果指定了就改变

不定长参数
def f(a,*b) #b的类型为元组

**kw：字典类型参数
def f(a,**b):
    print(a,b)
b={'3':9,'4':0}
f("kkk",**b)

函数可以作为参数
def g(a,b,f):
    return f(a+b)

```

lambda表达式：简化代码

```python
f=lambda x,y : x**y
print(f(2,10))

list1=lambda x:[i for i in range(x)]
```

global：全局变量想作用在函数内部，在函数内变量之前加global

```python
a=1
def f():
    global a+=1
```



装饰器：给caltime函数增加功能 @

```python
def caltime(f):
    s=time.time()
    f()
    t=time.time()
    return t-s

@caltime
def f():
    time.sleep(1)

print(f) # f不写括号


1.0003235340118408
```

闭包器

```python
def outer(a):
    b=10
    def inner(c):
        print(a+b+c)
    return inner
outer(2)(3)
```

生成器：为了节省空间

```python

yield 返回生成器
def f():
    for i in range(10):
        yield i
```

### 文件操作基础

```python
os.getcwd()
os.chdir()
a=os.path.realpath(__file__)
a=os.path.basename(a)
```



os输出文件路径

```python
import os
def searchpath(path):
    files=os.listdir(path)
    for f in files:
        fi_d=os.path.join(path,f) # 路径拼接
        if os.path.isdir(fi_d): # 如果fi_d是文件夹，递归查找下一层
            searchpath(fi_d)
        else: # 如果不是文件夹，输出路径/文件名
            print("->{}".format(fi_d))
searchpath(r"C:\Users\Zhaowei\Desktop\picture"+os.sep)
```

文本文件读写

```python
file=open(path,'r+',encoding="utf-8") #不存在，自动创建
r+:读写；a:在后面加
file.write('asdfghjkl')
file.close()
with open(path,'w') as f:
    f.write(...)
listing=file.read()
```

二进制文件读写

```python
wb
```

