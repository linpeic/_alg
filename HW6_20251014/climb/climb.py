import matplotlib.pyplot as plt
import numpy as np
# import gd

# x = np.array([0, 1, 2, 3, 4], dtype=np.float32)
# y = np.array([2, 3, 4, 5, 6], dtype=np.float32)

#爬山演算法改成下山演算法-->再進行線性回歸

x = np.array([0, 1, 2, 3, 4], dtype=np.float32)
y = np.array([1.9, 3.1, 3.9, 5.0, 6.2], dtype=np.float32)

def predict(a, xt):
	return a[0]+a[1]*xt

def MSE(a, x, y):
	total = 0
	for i in range(len(x)):
		total += (y[i]-predict(a,x[i]))**2
	return total
    #total沒有除len(x)，是因為爬山演算法只需關心那個方向更好，是否除不影響判斷

#先換成下山演算法
#哪個方向讓損失（MSE）降低，就往那個方向走 如果四個方向都沒有讓損失函數降低 就代表到局部最低點
def hillClimbingdown(f, x, y, h=0.01,round=1000):
    loops=0
    while (True):
        loops=loops+1
        if loops>round:
            break
        fxy = f(x, y)
        #print('x={0:.3f} y={1:.3f} f(x,y)={2:.3f}'.format(x, y, fxy))
        if f(x+h, y) <= fxy:
            x = x + h
        elif f(x-h, y) <= fxy:
            x = x - h
        elif f(x, y+h) <= fxy:
            y = y + h
        elif f(x, y-h) <= fxy:
            y = y - h
        else:
            break
    return (x,y,fxy)
#y=mx+b
#lambda m,b:MSE([m,b],x,y)是損失函數
m,b,_=hillClimbingdown(lambda m,b:MSE([m,b],x,y),0,0,h=0.01,round=1000)

# def loss(p):
# 	return MSE(p, x, y)

p = [0.0, 0.0]
# plearn = gd.gradientDescendent(loss, p, max_loops=3000, dump_period=1)

# Plot the graph
y_predicted = m+b*x
print('y_predicted=', y_predicted)
plt.plot(x, y, 'ro', label='Original data')
plt.plot(x, y_predicted, label='Fitted line')
plt.legend()
plt.show()
