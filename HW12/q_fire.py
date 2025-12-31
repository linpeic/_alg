import numpy as np
import math

def cross_entropy(p,q):
    r = 0
    for i in range(len(p)):
        #防止 log(0)
        q_safe = q[i] if q[i] > 1e-10 else 1e-10
        r=r+p[i]*math.log2(1/q_safe)
    return r

# 因為 q 的總和必須永遠是1不能直接隨機加減
# 我們必須 從一個元素扣掉數值 加到另一個元素
def get_neighbor(q_now,step_size):
    q_new =q_now.copy()
    #n_features=len(q_new)

    sub,bonus=np.random.choice(len(q_new),2,replace=False)
    value=np.random.uniform(0,step_size)
    value=min(value,q_new[sub])
    q_new[sub]=q_new[sub]-value
    q_new[bonus]=q_new[bonus]+value
    return q_new

#模擬退火法
def simulated_annealing(p,max_iter=2000, T_init=1.0, T_low=0.99, step_size=0.1):
    q_now=np.ones(len(p))/len(p) #[1/3,1/3,1/3]
    T = T_init
    mse_list= []
    q_best= q_now.copy()
    min_loss=cross_entropy(p, q_now)

    for i in range(max_iter):
        q_next=get_neighbor(q_now, step_size)
        mse_old=cross_entropy(p,q_now)
        mse_new=cross_entropy(p,q_next)
        mse_differ= mse_new-mse_old
        # mse_differ < 0 → （下坡）解較好（MSE 更小）
        # mse_differ > 0 → （上坡）解較差

        if mse_differ<0 or np.random.rand() < np.exp(-mse_differ/ T):
            #溫度 T 高時，差解容易被接受 → 幫助探索全局最佳、溫度 T 低時，只接受更好的解 → 收斂
            # np.exp()，計算 e 的 x 次方，MSE差越大 或 T越小 → 機率越小
            # np.random.rand() < np.exp(-mse_differ/ T)，有機率接受差解
            q_now = q_next #q_now最佳回歸參數
            if mse_new<min_loss:
                min_loss=mse_new
                q_best=q_next.copy()
        T=T*T_low
        mse_list.append(min_loss)
    return q_best, mse_list

p = np.array([0.27,0.42,0.31])
q_now_final,loss_historylist= simulated_annealing(p)
print(f"p:{p}")
print("q:", np.round(q_now_final,6))
print("final loss:", f"{loss_historylist[-1]:.6f}")
error=np.sum(np.abs(q_now_final-p))
print(error)
if error<0.01:
    print("q=p 收斂完成")
else:
    print("還沒完全收斂")
