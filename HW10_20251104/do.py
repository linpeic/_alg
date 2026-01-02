import numpy as np
import time

center_to_long=2 
n=4
#蒙地卡羅積分：隨機把點分布 再將原本的盒子體積*在目標內的比例 就會是目標體積
#參考資料：https://home.gamer.com.tw/creationDetail.php?sn=3981429
#黎曼積分:把不規則的形狀 切成無數個規則的小方塊 然後把這些方塊加起來


def monte_carlo(samples=1000000): #100000
    #length=2*center_to_long
    volume=(2*center_to_long)**n #算體積

    #生成隨機分布點 範圍是：中心延伸的範圍(-2~2)
    points=np.random.uniform(-center_to_long,center_to_long,(samples, n))

    #在裡面1 不再0 相+就可以知道有多少在裡面
    dist_sq=np.sum(points**2, axis=1)
    inside=np.sum(dist_sq<=1.0)
    
    return volume*inside/samples #體積*(裡面/全部)

def riemann(steps=20):

    d_long=(2*center_to_long)/steps#每小格的邊長
    dV= d_long**n  # 每個小格子的體積
    args = [0.0] * n  #[0.0, 0.0, 0.0, 0.0]
    def recursive_grid(dim_index):
        if dim_index==n:
            point = np.array(args)
            dist_sq = np.sum(point**2)
            if dist_sq<=1.0:
                return 1.0 #在裡面
            else:
                return 0.0 #不再
        
        val=-center_to_long+d_long/2.0
        total_sum = 0.0
        
        for _ in range(steps):
            args[dim_index]=val
            total_sum=total_sum+recursive_grid(dim_index+1)
            val=val+d_long
            
        return total_sum
    #print("總共",recursive_grid(0))
    return recursive_grid(0) * dV #從第一個為度(x軸)開始到結束的所有在目標中的點數
start=time.time()
monte=monte_carlo()
end=time.time()
print(f"蒙地卡羅積分{monte:.6f}，運行時間：{end-start:f}秒")
start=time.time()
rm=riemann()
end=time.time()
print(f"黎曼積分{rm:.6f}，運行時間：{end-start:f}秒")