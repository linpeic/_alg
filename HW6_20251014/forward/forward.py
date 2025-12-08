#參考：https://www.oryoy.com/news/ji-yu-python-de-xiang-qian-xuan-ze-suan-fa-zai-ji-qi-xue-xi-te-zheng-xuan-ze-zhong-de-ying-yong-yu-s.html

#向前演算法
#空集合 ->每次加入對模型而言最有幫助的(在這邊，選分數最高的。但是如果用於線性回歸，要選擇分數低的(誤差小)) ->加到不能再加為止(或者是有特定終止條件)
#向前演算法也可以選擇分數低的，依照我們想要解決的問題，去選擇，例如我要實作線性回歸，我要選擇分數低的
import random

#設定特徵集合
featureset_name= ['A','B','C','D']
featureset_value= [0.15, 0.43, 0.7, 0.38]


def getscore(set_value,set_name):
    score=0
    for value in set_value:
        score=score+value
        # if name in ['A','D','F']:
        #     score=score+1
    #加入些許誤差、干擾
    # error=random.uniform(-0.1,0.1)
    error=random.uniform(-0.01,0.01)
    score=score+error
    return score

def forward(featureset_name,featureset_value):
    select_name=[] #空集合
    select_value=[]
    choosing_name=featureset_name.copy()
    choosing_value=featureset_value.copy()
    best_score=-float('inf')#因為有干擾 有可能會<0，為了確保選擇時特徵會被選上

    while choosing_name:
        score=[]
        for value,name in zip(choosing_value,choosing_name):
            temp_name=select_name+[name]
            temp_value=select_value+[value]
            temp_score=getscore(temp_value,temp_name)
            score.append((temp_score,name,value))
        print(score)
# forward(featureset)
        score.sort(reverse=True)#分數高到低排列
        tuple_score,tuple_name,tuple_value=score[0]
        #只要分數比前一輪好就選入
        if tuple_score>best_score:
            select_name.append(tuple_name)
            select_value.append(tuple_value)
            choosing_name.remove(tuple_name)
            choosing_value.remove(tuple_value)
            best_score=tuple_score
        
        else:
            break
    return select_name,best_score 
finial_feature,finial_score=forward(featureset_name,featureset_value)
print("選擇的特徵",finial_feature)
print("分數",finial_score)