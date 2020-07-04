### pandas

Series：一维数组，每个元素有索引和值

```python
import pandas as pd
obj=pd.Series([2,1,7,-4,9]) #index默认为1,2,3,4,5
obj=pd.Series([2,1,7,-4,9],index=['a','b','c','d','e']) # 直接用值和索引生成
# 索引 值
# a    2
# b    1
# c    7
# d   -4
# e    9

dict={'a':2,'b':3,'c':4}
obj=pd.Series(dict) # 用字典生成
a    2
b    3
c    4
dtype: int64 #下面标注了类型
    
new_index=['a','b','c','d','e']
obj=pd.Series(dict,new_index) # 求new index对应的value，没有则为NaN
print(obj)
a    2.0
b    3.0
c    4.0
d    NaN
e    NaN
dtype: float64
    
print(obj1+obj2) #可以拼接两个数组
```

表格DataFrame

```python
df=pd.DataFrame(dict,columns,index)

csv=pd.read_csv('...csv')
dict={'name':['alice','bob','cathy','david'],
     'age':[16,17,18,19],
     'score':[90,91,93,94]}# 一种字典：按列输入
df=pd.DataFrame(dict)
#     name  age  score
# 0  alice   16     90
# 1    bob   17     91
# 2  cathy   18     93
# 3  david   19     94
df['num']=[1,2,3,4] # 添加一列num

print(df.iloc[0])# 获取第一行（索引必须是数字）
print(df.loc[1])# loc里面可以是字符串

df['flag']=np.nan # 新建一列空值，列名为flag
df['flag']=(df['name']=='bob')# 给新的列赋值，如果name=Bob，则c=True，否则填False


# 另一种字典：按行输入
dict={'english':{'alice':90,'bob':91},
      'math':{'alice':99,'bob':92}}
df=pd.DataFrame(dict)
#        english  math
# alice       90    99
# bob         91    92
print(df.index[1]) #根据索引取行
obj.reindex([]) #按照新的索引排序
```



```python
插值
method='ffill' #向前填充
method='bfill' #向后填充

import pandas as pd
import numpy as np
from pandas import Series,DataFrame
index1=pd.Index(range(3))
df=pd.DataFrame({'A':'O','B':'P','C':'Q'},index=index1)
df['D']=[1,np.nan,3]
print(df)
print(df.reindex(range(4),method='ffill'))
print(df)
```

```python
df=df.drop('rowname',axis=0) #删除行
df.drop('colname',axis=1)#删除列

df.add(dict,fill_value=0) df的缺失值=0后再和dict进行加法
```



横向表堆叠：两表合并

```python
df=pd.read_csv(r'C:\Users\Zhaowei\Desktop\暑假实训\数据\data.csv')
df1=df[['open','close']]
df2=df[['low','high']]
df=pd.concat([df1,df2],axis=1,join='outer并集/inner交集',)
axis：0竖向拼接（没有的属性填NaN）/1横向拼接（索引一一对应）
         close       high        low       open
0    2964.8421        NaN        NaN  2963.0186
1    3035.8741        NaN        NaN  2940.1916
2    3054.3030        NaN        NaN  3055.1535
3    3047.7035        NaN        NaN  3049.8747
4    3078.4759        NaN        NaN  3065.2307

          open      close        low       high
0    2963.0186  2964.8421  2953.2548  3000.4413
1    2940.1916  3035.8741  2935.8295  3036.8147
2    3055.1535  3054.3030  3035.9123  3061.7490
3    3049.8747  3047.7035  3038.5339  3055.5100
4    3065.2307  3078.4759  3062.8474  3117.9614

df3=df2.append(df1,ignore_index（新加的元组索引顺下来）=True) #直接加元组
```

主键合并（笛卡尔积）：merge

```python
import pandas as pd
df1=pd.DataFrame({'key':['a','b','c','b','c','a'],'data1':range(6)})
df2=pd.DataFrame({'key':['a','b','c','b','c'],'data1':range(5)})
df3=pd.merge(df1,df2,on='key',how='left')
  key  data1
0   a      0
1   b      1
2   c      2
3   b      3
4   c      4
5   a      5
  key  data1
0   a      0
1   b      1
2   c      2
3   b      3
4   c      4
  key  data1_x  data1_y
0   a        0        0
1   b        1        1
2   b        1        3
3   c        2        2
4   c        2        4
5   b        3        1
6   b        3        3
7   c        4        2
8   c        4        4
9   a        5        0

df1 has two b,whose values are 1 and 3
df2 has two b,whose values are 1 and 3
therefore, the merge frame has 4 rows whose key is 3
and [1,1],[1,3],[3,1],[3,3] 4 combinations
```

join

combine_first：保留第一章表，缺的再拿表2补

drop_duplicates(subset,keep,inplace):去重，keep：first/last,inplace=False不修改原表

```python
df1=pd.DataFrame({'key':['a','a','b','c'],'data1':['1','1','2','3']})
df3=df1.drop_duplicates()
```

# 特征重复:pear:Pearson相关系数:corr

```python
path=r'C:\Users\Zhaowei\Desktop\暑假实训\数据\future.csv'
df1=pd.read_csv(path)
print(df1)
print(df1[['RB','HC']].corr()) #钢筋、板材的相关度，越接近1相关性越高
#           RB        HC
# RB  1.000000  0.937514
# HC  0.937514  1.000000
```

#### :art: DataFrame可以直接绘图 :chart_with_upwards_trend:

```python
df['a','b'].plot() 
plt.show()
```

#### 缺失值（数值型用中位数、平均数填充，类别型用众数）

删除、插值法

### 标准化

离差标准化：将原始数据映射到[0,1]之间
$$
x'=\frac{x-min}{max-min}
$$

```python
path=r'C:\Users\Zhaowei\Desktop\暑假实训\数据\data.csv'
df=pd.read_csv(path)
f= lambda x: (x-x.min())/(x.max()-x.min())
df1=df[['close','vol','amount','return']]
print(df1.apply(f)) # 整张表标准化，apply
```

标准差标准化

小数定标标准化

哑变量处理pd.get_dummies：将非数值型数据转化为数值型（即bool01）

```
df=pd.DataFrame({'city':['a','a','b']})
print(df)
print(pd.get_dummies(df))
原：
  city
0    a
1    a
2    b
哑变量处理：
   city_a  city_b
0       1       0
1       1       0
2       0       1
```

离散化处理：将数据分成多个区间，一一对应

```python
pd.cut(df,bins=切分区间个数) #等宽分割

path=r'C:\Users\Zhaowei\Desktop\暑假实训\数据\data.csv'
df=pd.read_csv(path)
df1=df['close']
df=pd.cut(df1,bins=20)


groupby：按某种分割方法分组，之后可以计算每组均值等数据

path=r'C:\Users\Zhaowei\Desktop\暑假实训\数据\data.csv'
df=pd.read_csv(path)
df1=df['trade_date'] #获得日期的列
df1=pd.cut(df1,bins=3)
df3=df.groupby(df1) #按照平分3份的方法分组
print(df3['close'].mean()) #每组close属性的平均值
# trade_date
# (20190092.493, 20193605.333]    3756.699526
# (20193605.333, 20197107.667]            NaN
# (20197107.667, 20200610.0]      3932.088780
# Name: close, dtype: float64
```

transform：对所有元素进行一个操作

povit_table 透视表

