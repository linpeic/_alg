import cv2
#import sys
#sys.path.append("..")
import heapq
import utils
import numpy as np
import time
import cubic_spline 

class PlannerAStar:
    def __init__(self, m, inter=10):
        self.map=m
        self.inter = inter

    def initialize(self):
        self.queue = [] #存節點
        self.parent = {} #記錄父節點
        #f(n) = g(n) + h(n)
        self.h = {} # Distance from start to node
        self.g = {} # Distance from node to goal
        self.goal_node = None
        self.count=0
    #碰撞：看n1跟n2之間是否有障礙物
    def _check_collision(self, n1, n2):
        n1_ = utils.pos_int(n1)
        n2_ = utils.pos_int(n2)
        line = utils.Bresenham(n1_[0], n2_[0], n1_[1], n2_[1]) #n1 n2連線
        for pts in line:
            if self.map[int(pts[1]),int(pts[0])]<0.5:
                return True #代表撞牆
        return False #沒有撞牆
    #看自身位置可以走到那些節點 有八個方向
    def rounds(self,node,inter=10):
        rounds=[]
        x,y=node
        #周圍節點的範圍方向
        directions = [(-1, 0),(1, 0), (0, -1),(0, 1),(-1, -1),(-1, 1), (1, -1),(1, 1)]
        for nodex,nodey in directions:
            new_node=(x+nodex,y+nodey)
            # new_node=(x+nodex*inter,y+nodey*inter)
            if not self._check_collision(node, new_node) and utils.distance(node,new_node)<inter:
                    rounds.append(new_node)
        return rounds

    def planning(self, start=(100,200), goal=(375,520), inter=None, img=None):
        if inter is None:
            inter = self.inter
        start = (int(start[0]), int(start[1]))
        goal = (int(goal[0]), int(goal[1]))
        # Initialize 
        self.initialize()
        self.g[start] = 0
        self.h[start] = utils.distance(start, goal)
        #self.h[start] =abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        #self.queue.append((self.g[start] + self.h[start], start))
        self.parent[start] = None
        #自動排序好了
        heapq.heappush(self.queue, (self.g[start]+self.h[start], start))
        while(1):
            # A*
            #f(n) = g(n) + h(n)
            #g(n)：起點到當前節點的實際距離 h(n)：當前節點到目標節點的估計距離
            
            # min_cost=float('inf')
            # now_node=None
            #找成本最小的點
            min_cost, now_node = heapq.heappop(self.queue)
            self.count=self.count+1
            # for cost,min_node in self.queue:
            #      if cost <  min_cost:
            #         min_cost=cost
            #         now_node =min_node
            # self.queue.remove((min_cost,now_node))
            #找到目標的話
            if now_node == goal:
                self.goal_node = now_node
                break

            for round in self.rounds(now_node,inter):
                #如果周遭的點有 更小的成本(距離越短) 就更新
                temp_g =self.g[now_node] +utils.distance(now_node,round)
                if round not in self.g or temp_g<self.g[round]:
                        self.g[round]=temp_g
                        self.h[round] = utils.distance(round, goal)
                        #self.h[round]=abs(round[0]-goal[0])+abs(round[1]-goal[1])
                        #如果這個點之前沒有找過 需要預估一夏 他到終點的值
                        f =temp_g +self.h[round]
                        #self.queue.append((f, round))
                        heapq.heappush(self.queue, (f, round))
                        self.parent[round]=now_node 
        #紀錄會經過的點的座標
        path = []
        p = self.goal_node
        if p is None:
            return path
        while(True):
            path.insert(0,p)
            if self.parent[p] is None:
                break
            p = self.parent[p]
        if path[-1] != goal:
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
    m = 1-cv2.dilate(1-m, np.ones((20,20))) #讓障礙物變大 讓機器人可以跟表持距離 保留安全邊界
    img = img.astype(float)/255.

    start=(100,200)
    goal=(380,520)
    
    cv2.circle(img,(start[0],start[1]),5,(0,0,1),3)
    cv2.circle(img,(goal[0],goal[1]),5,(0,1,0),3)

    planner = PlannerAStar(m,20)
    start_time=time.time()
    path = planner.planning(start, goal, img=img)
    end=time.time()

    print(path)
    print(f"演算法運行時間:{end-start_time:.5f}")
    print("搜尋的節點數",planner.count)
    
    if path:
        for i in range(len(path)-1):
            cv2.line(img, utils.pos_int(path[i]), utils.pos_int(path[i+1]), (1,0,1), 2)
        
        draw_path = path[::25]
        
        if draw_path[-1] != path[-1]:
            draw_path.append(path[-1])

        path = np.array(cubic_spline.cubic_spline_2d(draw_path, interval=1))
        for i in range(len(path)-1):
            cv2.line(img, utils.pos_int(path[i]), utils.pos_int(path[i+1]), (1,0,0),2,cv2.LINE_AA)
        img_ = cv2.flip(img,0)
        cv2.imshow(f"A*",img_)
        k = cv2.waitKey(0)