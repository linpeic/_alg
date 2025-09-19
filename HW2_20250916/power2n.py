# 方法 1
n=25
def power2n(n):
    return 2**n
print("方法一",power2n(n))

# 方法 3：用遞迴+查表
mem= [None]*10000
def power2n4(n):
    if n==0:
        return 1
    if n==1:
        return 2
    if mem[n] is not None: 
        return mem[n]
    mem[n] = power2n4(n-1) + power2n4(n-1)
    return mem[n]
    # if ....
    # power2n(n-1)+power2n(n-1) 
print("方法三",power2n4(n))

# 方法 2a：用遞迴
def power2n2(n):
    if n==0:
        return 1
    if n==1:
        return 2
    return power2n2(n-1) + power2n2(n-1)
    # power2n(n-1)+power2n(n-1)
print("方法2a",power2n2(n))
# 方法2b：用遞迴
def power2n3(n):
    if n==0:
        return 1
    if n==1:
        return 2
    return 2*power2n3(n-1)
    # 2*power2n(n-1)
print("方法2b",power2n3(n))



