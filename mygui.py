import hashlib
import operator
import re

# 源文件 commentdata.txt
# 去除标点符号 delete_punctuation.txt
# MD5去重 outcome_md5.txt
# 机械压缩去词（循环）outcome_machine_compressed.txt
# 机械压缩去词（从开头）
# 机械压缩去词（从结尾）
# 形成list outcome_list.txt

path='C://Users//Zhaowei//Desktop//暑假实训//去重//'
ori_file='C://Users//Zhaowei//Desktop//暑假实训//去重//commentdata.txt'


# 小文本文件，用集合去重
def remove_duplicate(input_file,output_file):
    with open(input_file,'r',encoding="utf-8")as f:
        with open(output_file,'w',encoding="utf-8")as fp:
            data= [item.strip() for item in f.readlines()]
            newdata=list(set(data)) # 用集合去重
            fp.writelines(newdata)


def get_md5(data):
    md5=hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest


# 大文本文件，md5去重
def remove_duplicate_md5(input_file,output_file):
    str_set=set()
    with open(input_file,'r',encoding="utf-8")as f:
        with open(output_file,'a',encoding="utf-8")as fp:
            for line in f:
                line=line.strip()  # 去掉空格，否则md5会不同
                finger=get_md5(line)
                if finger not in str_set:
                    str_set.add(finger)
                    fp.write(line)
                fp.write('\n')


# 机械压缩分词（循环）
def machine_compressed(str1):
    for j in range(1,int(len(str1)/2)+1):# j是步长
        for i in range(len(str1)):
            if str1[i:i + j] == str1[i + j:i + 2*j]:
                k = i + j
                while str1[k:k + j] == str1[k + j:k + 2*j] and k < len(str1):  # k,k+2 k+2,k+4，从str1[i]开始的词和从str1[i+2]开始的词是否相同
                    k += j
                str1 = str1[:i]+str1[k:]
    return str1


def judge(l1,l2):  # 判断是否重复
    if len(l1) != len(l2):
        return False
    else:
        return operator.eq(l1,l2)


# 机械压缩分词（首尾）
def compressed(data):
    l1 = []
    l2 = []
    aim = []

    for i in data:
        if len(l1) == 0:
            l1.append(i)
        else:
            # l1首字符 与 新传进来的字符相同
            if l1[0] == i :
                if len(l2) == 0:
                    l2.append(i)
                else:
                    if judge(l1,l2):
                        l2.clear()
                        l2.append(i)
                    else:
                        aim.append(l1)
                        aim.append(l2)
                        l1.clear()
                        l2.clear()
                        l1.append(i)

            # l1首字符 与 新传进来的字符不相同
            else:
                if judge(l1,l2) and  len(l1)>1 :
                    aim.append(l1)
                    l1.clear()
                    l2.clear()
                    l1.append(i)

                else:
                    if len(l2) == 0:
                        l1.extend(i)
                    else:
                        l2.append(i)
    return aim

# 去除标点符号
def delete_punctuation(input_file,output_file):
    cnt = 0
    with open(input_file,'r',encoding="utf-8")as f:
        with open(output_file,'a',encoding="utf-8")as fp:
            for line in f:
                cnt += 1
                words=re.split(r'[;^!?.,！？。，：:（）()、；/\s]*', line)
                for word in words:
                    fp.write(word)
                fp.write('\n')
    return str

if __name__=="__main__":
    # print("start delete_punctuation")
    # delete_punctuation(ori_file,path+"delete_punctuation.txt")
    #
    # print("start remove_duplicate_md5")
    # remove_duplicate_md5(path+"delete_punctuation.txt",path+'outcome_md5.txt')
    #
    # print("start machine_compressed")
    with open(path + 'outcome_machine_compressed.txt', 'w', encoding="utf-8")as fp:
        fp.write('')
    cnt=0
    with open(path+'outcome_md5.txt','r',encoding="utf-8")as f:
        with open(path+'outcome_machine_compressed.txt','a',encoding="utf-8")as fp:
            for line in f:
                cnt+=1
                line=line.strip()
                fp.write(machine_compressed(line))
                fp.write('\n')
                print("line %d has been handled..."%cnt)
    strr=""
    with open(path+'outcome_machine_compressed.txt','r',encoding="utf-8")as f:
        for line in f:
            strr+=line.strip()
    strr=compressed(strr) # 正向压缩
    str_reverse=strr[::-1]
    str_reverse=compressed(str_reverse) # 反向压缩
    list_str=str_reverse[::-1]





