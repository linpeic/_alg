import cv2
import numpy as np
# import sys
# sys.path.append("..")
import utils
import numpy as np
import time
import cubic_spline 

class PlannerRRT:
    def __init__(self, m, extend_len=60):
        #20
        self.map=m
        self.extend_len = extend_len

    def _random_node(self, goal, shape):
        r = np.random.choice(2,1,p=[0.5,0.5])
        if r==1:
            return (float(goal[0]), float(goal[1]))
        else:
            rx = float(np.random.randint(int(shape[1])))
            ry = float(np.random.randint(int(shape[0])))
            return (rx, ry)
    #尋找最近的節點 把它當作樹生長得起點
    def _nearest_node(self, samp_node):
        min_dist = 99999
        min_node = None
        for n in self.ntree:
            dist = utils.distance(n, samp_node)
            if dist < min_dist:
                min_dist = dist
                min_node = n
        return min_node
    #檢查兩點是碰撞 出發點跟找到的新生長點
    def _check_collision(self, n1, n2):
        n1_ = utils.pos_int(n1)
        n2_ = utils.pos_int(n2)
        line = utils.Bresenham(n1_[0], n2_[0], n1_[1], n2_[1])
        for pts in line:
            if self.map[int(pts[1]),int(pts[0])]<0.5:
                return True
        return False
    #途中綠色的分支
    def _steer(self, from_node, to_node, extend_len):
        vect = np.array(to_node) - np.array(from_node)
        v_len = np.hypot(vect[0], vect[1])
        v_theta = np.arctan2(vect[1], vect[0])
        if extend_len > v_len:
            extend_len = v_len
        new_node = (from_node[0]+extend_len*np.cos(v_theta), from_node[1]+extend_len*np.sin(v_theta))
        #如果超出邊界 或會撞牆
        if new_node[1]<0 or new_node[1]>=self.map.shape[0] or new_node[0]<0 or new_node[0]>=self.map.shape[1] or self._check_collision(from_node, new_node):
            return False, None
        else:        
            return new_node, utils.distance(new_node, from_node)

    def planning(self, start, goal, extend_len=None, img=None):
        if extend_len is None:
            extend_len = self.extend_len
        self.ntree = {} #新節點=父節點，儲存：(key: 節點, value: 父節點)
        self.ntree[start] = None#設定起點的父節點為none(根節點)
        self.cost = {} #儲存每個節點得成本
        self.cost[start] = 0 #起點成本為0
        goal_node = None #goal的前一個點
        self.count=1
        for it in range(10000):
            print("\r", it, len(self.ntree), end="")
            samp_node = self._random_node(goal, self.map.shape)
            near_node = self._nearest_node(samp_node)#找最近的點
            new_node, cost = self._steer(near_node, samp_node, extend_len) #找到的那個點去做延伸
            if new_node is not False:
                self.ntree[new_node] = near_node
                self.cost[new_node] = cost + self.cost[near_node]
                self.count=self.count+1
            else:
                continue
            if utils.distance(near_node, goal) < extend_len:
                goal_node = near_node#把倒數第二個點 記錄起來 因為等等回朔時才可以知道 要從哪開始
                break
    
            # 畫成像樹的分散圖
            if img is not None:
                for n in self.ntree:
                    if self.ntree[n] is None:
                        continue
                    node = self.ntree[n]
                    cv2.line(img, (int(n[0]), int(n[1])), (int(node[0]), int(node[1])), (0,0.5,0.5), 1)
                # Draw Image
                img_ = cv2.flip(img,0)
                cv2.imshow("rrt",img_)
                k = cv2.waitKey(1)
                if k == 27:
                    break
        
        #紀錄會經過的點的座標
        path = []
        n = goal_node
        while(True):
            path.insert(0,n)
            if self.ntree[n] is None:
                break
            node = self.ntree[n]
            n = self.ntree[n] 
        path.append(goal)
        return path

if __name__ == "__main__":
    #讓電腦看懂地圖
    img = cv2.flip(cv2.imread("D:/ccc/ccc114a_Algorithm/_alg/mid/maps/map_U.png"),0)
    #非黑即白分類
    img[img>128] = 255 #淺色->全白
    img[img<=128] = 0#深色->全黑
    m = np.asarray(img)
    m = cv2.cvtColor(m, cv2.COLOR_RGB2GRAY)
    m = m.astype(float) / 255.
    m = 1-cv2.dilate(1-m, np.ones((20,20)))
    #讓障礙物變大 讓機器人可以跟表持距離 保留安全邊界
    img = img.astype(float)/255.

    
    start=(100,200)
    goal=(380,520)
    
    cv2.circle(img,(start[0],start[1]),5,(0,0,1),3)
    cv2.circle(img,(goal[0],goal[1]),5,(0,1,0),3)
    
    planner = PlannerRRT(m,60)
    start_time=time.time()
    path = planner.planning(start, goal, img=img)
    end=time.time()
    
    print(path)
    print(f"演算法執行時間:{end-start_time}")
    print("搜尋的節點數",planner.count)
    
    # Extract Path
    
    for i in range(len(path)-1):
        cv2.line(img, utils.pos_int(path[i]), utils.pos_int(path[i+1]), (1,0,1), 2)
    if planner.count>2:
        path = np.array(cubic_spline.cubic_spline_2d(path, interval=0.5))
        for i in range(len(path)-1):
            cv2.line(img, utils.pos_int(path[i]), utils.pos_int(path[i+1]), (1,0,0), 2)
    
    img_ = cv2.flip(img,0)
    cv2.imshow(f"rrt",img_)
    k = cv2.waitKey(0)