# 基于Keras的Sequential模型建模，预测新的评论是好评还是差评

import pandas as pd
import jieba
import tensorflow
from gensim.models import word2vec
import keras
from keras import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM,GRU
from keras.layers.core import Dense,Dropout,Activation
from tensorflow.keras.preprocessing import sequence
import gensim
import numpy as np
import xlwt
from sklearn.model_selection import train_test_split
path=r'C:\Users\Zhaowei\Desktop\暑假实训\去重\0707'
def read_data():
    print("start read_data")
    ng=pd.read_excel(path+'\score=0.xlsx',header=None,index=None)  # 差评
    ps=pd.read_excel(path+'\score=1.xlsx',header=None,index=None)  # 好评
    ng['mark']=-1
    ps['mark']=1
    pn=pd.concat([ng,ps],ignore_index=True)

    x=pn[1]  # 下标取决于文本存在哪一列
    y=pn['mark']    # 设标签
    return x,y
# 删除停用词
def del_stop_word(sentences):
    print("start del_stop_word")
    with open(r'C:\Users\Zhaowei\Desktop\暑假实训\去重\0709\stoplist.txt', 'r', encoding='utf-8')  as fp:
        stop_words = fp.readlines()
        stop_words = [stop_word.replace('\n', '') for stop_word in stop_words]
    new_sentences=[]
    for line in sentences:
        line=str(line)
        for stop_word in stop_words:
            if stop_word in line:
                line = line.replace(stop_word, '')
        new_sentences.append(line)
    return new_sentences

def remove_words(sentences):
    print('start remove_words')
    model = gensim.models.Word2Vec.load("word2vec.model")
    for i, line in enumerate(sentences):
        for word in line:
            if word not in model.wv.vocab:
                line.remove(word)
                sentences[i] = line
    return sentences

def get_words_jieba(sentences):
    print("start get_words_jieba")
    model = gensim.models.Word2Vec.load("word2vec.model")
    all_aim_word = {}
    while True:
        words_after_jieba = [[word for word in jieba.cut(line) if word.strip()] for line in sentences]
        new_words = []
        for line in words_after_jieba:
            for word in line:
                if word not in model.wv.vocab and word not in all_aim_word.keys():
                    all_aim_word[word] = 1
                    new_words.append(word)
                elif word not in model.wv.vocab:
                    all_aim_word[word] += 1
        # 如果剩余的新词小于我们设置的阈值，返回分词结果。否则删除新词（del_word)
        if len(new_words) < 10:
            for word in new_words:
                print('new_word', word)
            for word in all_aim_word:
                if all_aim_word[word] > 5:
                    print(word, all_aim_word[word])
            return words_after_jieba

        else:
            for word in new_words:
                jieba.del_word(word)

# 加入词向量
def form_embedding(sentences,model_path="word2vec.model"):
    model = gensim.models.Word2Vec.load(model_path)
    # index2word词列表，vectors词向量数组，
    w2v = dict(zip(model.wv.index2word, model.wv.vectors))

    w2index = {}
    index = 1
    for sentence in sentences:
        for word in sentence:
            if word not in w2index:
                w2index[word] = index
                index += 1
    print("文本中总共有{}个词".format(len(w2index)))

    # 建立词语到词向量的映射
    embeddings = np.zeros(shape=(len(w2index) + 1, 256), dtype=float)  # 256指的是一条评论最多含有的词数
    embeddings[0] = 0

    n_not_in_w2v = 0
    # 词语，频数
    for word, index in w2index.items():
        if word in model.wv.vocab:
            embeddings[index] = w2v[word]
        else:
            print("not in w2v: %s" % word)
            n_not_in_w2v += 1
    print("words not in w2v count: %d" % n_not_in_w2v)

    del model, w2v

    # 每个句子的词向量
    x = [[w2index[word] for word in sentence] for sentence in sentences]

    return embeddings, x

# 切分数据集，训练集与测试集8:2
def split_train_data(x,y):
    x_train,x_val,y_train,y_val=train_test_split(x,y,test_size=0.2)

    x_train=sequence.pad_sequences(x_train,max_length)  # 超长部分取0
    x_val=sequence.pad_sequences(x_val,max_length)

    y_train=keras.utils.to_categorical(y_train,num_classes=2)  # y有1和-1两类
    y_val=keras.utils.to_categorical(y_val,num_classes=2)

    return x_train,x_val,y_train,y_val

if __name__== '__main__':
    x,y=read_data()
    x = x.values.tolist()   # 转成list
    y = y.values.tolist()
    x=del_stop_word(x)
    x=get_words_jieba(x)
    x=remove_words(x)
    embeddings,x=form_embedding(x)  # 建立词向量映射
    max_length=max([len(line)for line in x])
    print(max_length)
    # x_train->y_train是训练集，x_val->y_val是测试集，把x_val带入建好的模型中得到的结果与y_val进行比较
    x_train, x_val, y_train, y_val=split_train_data(x,y)


    print('build model...')
    model=Sequential()  # 初始化模型obj
    # 神经网络的层：Embedding（词向量的数量，词向量的长度（维度），序列的数量）
    model.add(Embedding(len(embeddings),len(embeddings[0]),input_length=max_length))
    model.add(LSTM(30))  # 隐藏层降维
    model.add(Dropout(0.5)) # 避免过拟合
    model.add(Dense(1))  # 隐藏层
    model.add(Activation('softmax'))    # 归一化
    
    # 模型编译（损失函数，优化器）
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.fit(x_train,y_train,batch_size=30)    # 训练，传入训练集
    pre=model.predict_classes(x_val,batch_size=30)  # 预测
    score=model.evaluate(pre,y_val,batch_size=30)  # 用预测值pre和实际值y_val进行评估
    print(pre)
    print(score)



