import os,jieba,re
from collections import Counter,defaultdict
import pickle

class GetPro():
    def __init__(self):
        self.normalWord = []        #正常邮件中的词[{},{}...{}]
        self.trashWord = []        #垃圾邮件中的词
        self.words = []             #所有出现过的单词
    def getWord(self):
        """
        获取邮件中的词
        :return:
        """
        confiles = os.listdir('./data')  #词的分类
        for dirname in confiles:
            path = "./data/"+dirname
            for filename in os.listdir(path):
                self.splitWord(path+'/'+filename,dirname)

    def splitWord(self,filename,type):
        """
        :param filename: 邮件路径
        :param type: 邮件类型
        :return: None
        """
        with open(filename,"r",encoding="gbk",errors='ignore') as f:
            con = f.read() #邮件内容
            index = con.index("\n\n")#过滤无用内容，index检验是否包含（）内容
            con = con[index:]#切片
            con = con.replace("\n","").strip()#去除两端不需要的地方
            r = re.compile("[^\u4e00-\u9fa5]+")#正则匹配
            con = r.sub("",con)#直接取反拿字符串
            con = jieba.cut(con,cut_all=False)#jieba切
            words =[word for word in con if len(word) >= 2]
            if type == "normal":
                self.normalWord += list(set(words))
            else:
                self.trashWord += list(set(words))
            self.words += words

    def getRatio(self):
        data = defaultdict(list)
        normalWord = Counter(self.normalWord)
        trashWord = Counter(self.trashWord)
        for word in set(self.words):
            if word in self.normalWord:
                num = normalWord[word]
                num2 = trashWord[word]
                arr = [num,num2]
                for i in arr:
                    if i != 0:
                        data[word].append(i/8000)
                    else:
                        data[word].append(0.00001)
        print(data)
        with open("ratio.txt","wb+") as f:
            pickle.dump(data,f)



obj = GetPro()
obj.getWord()
obj.getRatio()
