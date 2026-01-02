import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import platform

featureset_name = ['A', 'B', 'C', 'D']
X_np = np.array([
    [0.15, 0.43, 0.70, 0.38],
    [0.20, 0.40, 0.65, 0.42],
    [0.18, 0.45, 0.68, 0.39],
    [0.22, 0.42, 0.72, 0.37],
    [0.19, 0.44, 0.66, 0.40]
], dtype=np.float32)

y = np.array([1.9, 3.1, 3.9, 5.0, 6.2], dtype=np.float32)
X_data = pd.DataFrame(X_np, columns=featureset_name)
#原本的公式 1-(RSS/TSS) RSS:模型預測值和真實值差的平方總和 TSS:觀察值和平均值差的平方總和(表示原本資料的變異量)
#https://medium.com/qiubingcheng/%E5%9B%9E%E6%AD%B8%E5%88%86%E6%9E%90-regression-analysis-%E7%9A%84r%E5%B9%B3%E6%96%B9-r-squared-%E8%88%87%E8%AA%BF%E6%95%B4%E5%BE%8Cr%E5%B9%B3%E6%96%B9-adjusted-r-squared-f38ad733bc4e
#因為會有過度擬合的狀況發生，就是加入沒有用的特徵，也會使數值變大
#因此使用調整過後的R平方，他考慮了納入的特徵數量
#公式 1-(1-R²)(n-1)/(n-k-1)
#因此即便納入沒用的特徵，也會直接被淘汰
def score_adj_r2(feature_test, X, y):
  
    n = len(y)
    k = len(feature_test) # k = 特徵數
    
    if k == 0:
        return 0.0 # 空模型的 Adj. R² 為 0

    if (n-k-1)<= 0:
        return -float('inf') 
    #使用 sklearn 函式庫訓練一個模型，然後計算這個模型的 R 平方
    model = LinearRegression()
    X_subset = X[feature_test]#選出要測試的特徵
    model.fit(X_subset, y)
    r2 = model.score(X_subset,y)
    
    # 計算 調整R²
    adj_r2 =1-(1-r2)*(n-1)/(n-k-1)
    
    return adj_r2

#找分數高
def forward(featureset_name, X, y):
    select_name = []
    choosing_name = featureset_name.copy()
    best_score = -float('inf') 
    
    # # 先計算一次空模型的分數 (Adj. R²)
    # best_score = score_adj_r2(select_name, X, y) # 這會回傳 0
    # print(f"--- 開始向前演算法 (使用 Adjusted R²) ---")
    # print(f"初始模型 (僅截距) Adj. R²: {best_score:.4f}\n")

    while choosing_name:
        score_list=[] #儲存(adj_r2,name)
        for name in choosing_name:
            temp_name=select_name+[name]
            temp_score=score_adj_r2(temp_name, X, y)
            score_list.append((temp_score,name))
        print("分數",score_list)

        score_list.sort(reverse=True) #大到小排序
        tuple_score,tuple_name=score_list[0] #最高分的
        
        if tuple_score>best_score:
            select_name.append(tuple_name)
            choosing_name.remove(tuple_name)
            best_score = tuple_score
            
        else:
            break
        print("select:",select_name)    
    return select_name, best_score


finial_feature, finial_score = forward(featureset_name, X_data, y)

if finial_feature:
    X_final_subset = X_data[finial_feature]
    final_model = LinearRegression()
    final_model.fit(X_final_subset, y)
    y_final_pred = final_model.predict(X_final_subset)

system_name = platform.system()
if system_name == "Windows":  
    # Windows 使用微軟正黑體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.figure(figsize=(8, 8))
    plt.scatter(y, y_final_pred, alpha=0.7, label='模型預測 vs 實際')
    min_val = min(y.min(), y_final_pred.min())
    max_val = max(y.max(), y_final_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='完美預測 (y=x)')
    plt.title(f'最終模型表現 (特徵: {finial_feature})')
    plt.xlabel('實際 y 值')# y_true
    plt.ylabel('模型預測 y 值 ')#y_pred
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()
