import cv2
import numpy as np
img = cv2.imread("D:/ccc/ccc114a_Algorithm/_alg/mid/maps/map_U.png")

dots =[]   # 記錄座標的空串列
click = 1
def set_start_goal(event,x,y,flags,param):
    global click
    if event == 1:
        img_color=img[y,x]
        
        if click==1:
            if np.mean(img_color)<128:
                print("障礙物，請重新設定起點")
                return
            dots.append([x, y])                          # 記錄座標
            cv2.circle(img, (x, y), 10, (0,255,0), -1)   # 在點擊的位置，繪製圓形
           
            cv2.imshow('A*', img)
            click=click+1
            start = tuple(dots[0])
            print(start)
            # print(click)
        elif click ==2:
            if np.mean(img_color)<128:
                print("障礙物，請重新設定終點")
                return
            dots.append([x, y])                          # 記錄座標
            cv2.circle(img, (x, y), 10, (0,0,255), -1)   # 在點擊的位置，繪製圓形
            
            cv2.imshow('A*', img)
            click=click+1
            # print(dots[1])
            goal= tuple(dots[1])
            print(goal)
        # elif click>=3:
        #     print("路徑規劃")
    
cv2.imshow('A*', img)
cv2.setMouseCallback('A*',set_start_goal)

cv2.waitKey(0)
cv2.destroyAllWindows()