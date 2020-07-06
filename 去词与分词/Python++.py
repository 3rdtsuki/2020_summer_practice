import jieba
import jieba.analyse as analyse
import jieba.posseg as peseg
path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
ori_file='C://Users//Zhaowei//Desktop//暑假实训//去重//outcome_machine_compressed.txt'
output_file=path+'jieba.txt'

stopwords=['的','了','与','是','得']  # 停用词
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