# 冒泡：两个相比，大的往后，大的为泡，冒到最后

# 冒泡排序：比较第一个第二个，大的放后面，比较第二个第三个，大的放后面，以此类推，比到n-1，实现列表中最大的到达最后面，像冒一次泡，
#           再比较第一个第二个，像之前那样再来一次，比到n-2，实现剩余列表中最大的到达倒数第二为，又冒一次泡
#           以此类推，实现由小到大排序
# l = [1,2,3,4,5,6.....n]


"""
-  -  -  -  -  -
-  -  -  -  -  *
-  -  -  -  *  *
-  -  -  *  *  *
-  -  *  *  *  *
-  *  *  *  *  *
"""

l = [3,6,9,3,6,8,1,5,8]
def bubble_sort(l):
    n = len(l)
    for i in range(n-1,0,-1):
        for j in range(i):
            if l[j] > l[j+1]:
                l[j],l[j+1] = l[j+1],l[j]
    return l

print(bubble_sort(l))

# 优化，降低复杂度：思路是如果某次冒泡没有任何交换，说明已经是从小到大排序好的，直接return

l = [3,6,9,3,6,8,1,5,8]
def bubble_sort(l):
    n = len(l)
    for i in range(n-1,0,-1):
        c = 0                                # c为交换次数
        for j in range(i):
            if l[j] > l[j+1]:
                c += 1
                l[j],l[j+1] = l[j+1],l[j]
        if c == 0:                          # 如果一次冒泡交换次数为0，直接return
            return l


print(bubble_sort(l))









def bubble_sort(l):
    n = len(l)
    for j in range(n-1,0,-1):
        c = 0
        for i in range(0,j):
            if l[i] > l[i+1]:
                l[i],l[i+1] = l[i+1],l[i]
                c += 1
        if c == 0 :
            return l
    return l
l = [2,1,3,5,4,6]
print(bubble_sort(l))
























