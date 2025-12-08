import numpy as np
import matplotlib.pyplot as plt
import platform

#爬山法只走「上坡」→ 容易卡局部
#模擬退火法允許「偶爾下坡」→ 增加找到全局最佳的機會。
'''
模擬退火法是一種隨機化的全域最佳化演算法，靈感來自物理退火（annealing）過程：

金屬加熱後慢慢冷卻 → 原子從高能量狀態逐漸穩定到低能量晶格 → 最終達到全局最低能量

在演算法中：我們把目標函數（例如誤差、能量）當成「能量」，希望利用降溫過程找到全局最優解（最優解）
'''
# 模擬資料
# np.random.seed(0)
X = np.array([[1,1],[1,2],[1,3],[1,4]]) #輸入
# y = np.array([2,3,4,5])
noise = np.random.normal(0,0.3, 4) 
#np.random.normal(mean, std, n) → 生成 n 個服從常態分布的隨機數
# 產生 4 個平均為 0,標準差為 0.3 的干擾，因為要更符合實際狀況
y = np.array([2, 3, 4, 5]) + noise #輸出

def predict(a, xt):
	return np.dot(a, xt)
#二維矩陣
def MSE(a, X, y):
	total = 0
	for i in range(len(X)):
		total += (y[i]-predict(a,X[i]))**2
	return total/len(X)
    #有除len(x)，因為模擬退火法的MSE通常定義為平均誤差

# 模擬退火法
def simulated_annealing(X, y, max_iter=1000, T_init=1.0, T_low=0.99, step_size=0.1):
    n_features = X.shape[1]#2D 二維矩陣[1,1]
    best= np.random.randn(n_features) 
    T = T_init
    mse_list= []

    for i in range(max_iter):
        best_new= best +np.random.uniform(-step_size, step_size,size=n_features)
        #np.random.uniform(low, high, size) 探索鄰近解空間，尋找可能更小的 MSE
        mse_old=MSE(best, X, y)
        mse_new=MSE(best_new, X, y)
        mse_differ= mse_new-mse_old
        # mse_differ < 0 → 解較好（MSE 更小）
        # mse_differ > 0 → 解較差

        if mse_differ<0 or np.random.rand() < np.exp(-mse_differ/ T):
            #溫度 T 高時，差解容易被接受 → 幫助探索全局最佳、溫度 T 低時，只接受更好的解 → 收斂
            # np.exp()，計算 e 的 x 次方，MSE差越大 或 T越小 → 機率越小
            # np.random.rand() < np.exp(-mse_differ/ T)，有機率接受差解
            best = best_new #best最佳回歸參數
        T=T*T_low
        mse_list.append(MSE(best,X,y))
    return best, mse_list

# 執行模擬退火
best_finial, mse_list= simulated_annealing(X, y)

print("模擬退火求出的best:", best_finial)
print("最終 MSE:", mse_list[-1])

system_name = platform.system()
if system_name == "Windows":  
    # Windows 使用微軟正黑體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False

# 畫回歸圖
plt.figure(figsize=(8,5))

# 散點圖
plt.scatter(X[:,1], y, color='blue', label='Data')

# 模擬退火回歸線
x_line = np.linspace(min(X[:,1])-0.5, max(X[:,1])+0.5, 100)
y_line = best_finial[0] + best_finial[1]*x_line
plt.plot(x_line, y_line, color='red', label='回歸線')

plt.xlabel('X')
plt.ylabel('y')
plt.title('模擬退火演算法回歸圖')
plt.legend()
plt.grid(True)
plt.show()
