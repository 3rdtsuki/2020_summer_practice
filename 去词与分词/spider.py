from gensim.models import word2vec
path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
ori_file='C://Users//Zhaowei//Desktop//暑假实训//去重//outcome_machine_compressed.txt'
output_file=path+'jieba.txt'

sentences=[]
with open(output_file,'r',encoding='utf-8')as fp:
    for line in fp:
        line=line.strip().split(' ')
        item=[]
        for i in line:
            item.append(i)
        sentences.append(item)

# size:向量维度，min_count：低于该频度不做词向量
model=word2vec.Word2Vec(sentences,size=256,min_count=1)
model.save('word2vec.model')
print(model.wv.similarity('好看','漂亮'))