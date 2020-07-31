### jieba分词

```python
import jieba
seg1=jieba.cut(text,cut_all=True)  # 全模式
print('/'.join(seg1))
seg2=jieba.cut(text,cut_all=False)  # 精确模式
# cut_all默认为False
f.write('/'.join(seg2))
seg3=jieba.cut_for_search(text)  # 搜索引擎模式：介于1,2之间
print('/'.join(seg3))

jieba.del_word('')
del_dict=['aa','bb']
for i in del_dict:
    jieba.del_word(i)
    
jieba.load_userdict(file)
jieba.suggest_freq()词频>n时分割出来
```

保留、删除分词：

```python
import jieba
path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
ori_file='C://Users//Zhaowei//Desktop//暑假实训//去重//commentdata.txt'

# 要保留的完整的词
with open(path + 'add_dict.txt', 'w', encoding='utf-8')as fp:
    add_dict = ['荣耀独特'] 
    for i in add_dict:
        fp.write(i)
        fp.write('\n')
jieba.load_userdict(path + 'add_dict.txt')

# 要删除的词
with open(path+'del_dict.txt','w',encoding='utf-8')as fp:
    del_dict=['藏式','像头']
    for i in del_dict:
        fp.write(i)
        fp.write('\n')
        jieba.del_word(i)
        
        
cnt=0
with open(ori_file,'r',encoding='utf-8')as fp:
    for line in fp:
        cnt+=1
        text=str(line)
        seg2=jieba.cut(text,cut_all=True)  # 精确模式
        print('/'.join(seg2))
        if cnt>20:
            break
```


$$
TF(词频) = \frac{词出现的个数}{总词数}
$$

$$
IDF = log(\frac{总文本数}{含有该词的文本数})
$$

$$
TF-IDF = TF1*IDF1 + TF2*IDF2 + ....+ TFn* IDFn
$$
提取关键字：

```python
import jieba
import jieba.analyse as analyse
text='它的外观设计非常年轻化，线条硬朗的磨砂质感全金属机身触感舒适，原本比较单调素雅的配色在增加了A面CNC钻石切割的小蓝边设计和淡蓝色镂空Logo后，辨识度提高了不少。'
# TF-IDF提取关键字（基于词频）
tfidf=jieba.analyse.extract_tags
keywords=tfidf(text)
for i in keywords:
    print(i+'/',end="")
    
磨砂/度提高/CNC/蓝边/Logo/素雅/配色/全金属/触感/淡蓝色/外观设计/镂空/年轻化/辨识/硬朗/质感/单调/机身/钻石/线条/

# textrank提取关键字（类似pagerank，基于相邻词语的关联性）
textrank=analyse.textrank
keywordlist=textrank(text)
for i in keywordlist:
    print(i+'/',end="")
    
设计/小蓝边/触感/机身/质感/磨砂/镂空/线条/配色/全金属/原本/淡蓝色/钻石/切割/辨识/单调/年轻化/外观设计/增加/度提高/

# 词性标注
import jieba.posseg as peseg
words=peseg.cut('我是南开大学学生')
for word ,flag in words:
    print(word+':'+flag)
    
我:r
是:v
南开大学:nt
学生:n
词性表见：https://blog.csdn.net/enter89/article/details/80619805
```

停用词：

```python
import jieba
import jieba.analyse as analyse
import jieba.posseg as peseg
path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
ori_file='C://Users//Zhaowei//Desktop//暑假实训//去重//outcome_machine_compressed.txt'
output_file=path+'jieba.txt'

stopwords=['的','了','与']  # 停用词
def seg_list(text):
    text_depart=jieba.cut(text.strip())
    outstr=''
    for word in text_depart:
        if word not in stopwords:
            if word != '\t':
                outstr+=word+' '
    return outstr

if __name__=="__main__":
    with open(output_file, 'w', encoding='utf-8')as f:
        f.write('')
    with open(ori_file,'r',encoding='utf-8') as fp:
        with open(output_file,'a',encoding='utf-8')as f:
            for line in fp:
                f.write(seg_list(line))
                f.write('\n')
```

### 词向量：词->向量，用来表示词之间的关系

word2vec方法（在gensim.models库中）

one-hot编码：[001,010,100]代表3种状态的特征

对于一句话可以拆成多个特征，即多段onehot编码，组合起来形成向量

于是向量距离小的词向量，相似度高

```python
path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
output_file=path+'jieba.txt'

sentences=[]  # 获得训练集，是一个二维数组，每行是一句话
with open(output_file,'r',encoding='utf-8')as fp:
    for line in fp:
        line=line.strip().split(' ')
        item=[]
        for i in line:
            item.append(i)
        sentences.append(item)
        
from gensim.models import word2vec
# size:向量维度，min_count：低于该频度不做词向量
model=word2vec.Word2Vec(sentences,size=256,min_count=1)  # 训练
model.save('word2vec.model')  # 生成的模型保存在代码同级目录
print(model.wv.similarity('好看','漂亮'))  # 分析相似度
```

