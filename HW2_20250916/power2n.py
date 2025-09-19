# 方法 1
n=20
def power2n(n):
    return 2**n
print("方法一",power2n(n))
# 方法 2a：用遞迴
def power2n2(n):
    return power2n(n - 1) + power2n(n - 1)
    # power2n(n-1)+power2n(n-1)
print("方法二",power2n2(n))
# 方法2b：用遞迴
def power2n3(n):
    return 2*power2n(n - 1)
    # 2*power2n(n-1)
print("方法三",power2n3(n))
# 方法 3：用遞迴+查表
def power2n4(n):
    if not power2n(n) is None: return power2n(n) 
    return power2n(n - 1) + power2n(n - 1)
    # if ....
    # power2n(n-1)+power2n(n-1) 
print("方法四",power2n4(n))
