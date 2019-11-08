"""
获取邮件内容
邮件分词
通过贝叶斯算法计算邮件是垃圾邮件的概率
"""
#获取ratio数据
import pickle,jieba,re

with open('ratio.txt','rb+') as f:
    ratio = pickle.load(f)

with open('data/normal/12','r',encoding='gbk',errors='ignore') as f:
    email = f.read()

def GetRatio(con):
    index = con.find("\n\n") if con.find("\n\n")>0 else 0 # 过滤无用内容，index检验是否包含（）内容
    con = con[index:]  # 切片
    con = con.replace("\n", "").strip()  # 去除两端不需要的地方
    r = re.compile("[^\u4e00-\u9fa5]+")  # 正则匹配
    con = r.sub("", con)  # 直接取反拿字符串
    con = jieba.cut(con, cut_all=False)  # jieba切
    words = [word for word in con if len(word) >= 2]

    p = 1
    rest_p = 1
    for word in words:
        if word in ratio:
            p *= ratio[word][1] #word词 是垃圾邮件的概率
            rest_p *= 1-ratio[word][1]

    P = p/(p+rest_p)
    # print(P)

    p1 = 1
    rest_p1 = 1
    for word in words:
        if word in ratio:
            p1 *= ratio[word][0]  # word词 是正常邮件的概率
            rest_p1 *= 1 - ratio[word][0]

    P1 = p1/(p1 + rest_p1)
    # print(P1)

    if P>P1:
        return False
    else:
        return True

GetRatio(email)
