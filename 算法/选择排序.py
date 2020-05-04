
# 选择：从后面选出一个

# 选择排序：在一个列表里选出一个最小的放最前面，在剩下的里面再选出一个放最前面，以此类推，实现排序
#           怎么选最小的呢，默认以第一个数的索引为最小数索引，依次和后面的比较，如果遇见更小的，选择更小的索引为最小数索引，
#           依次类推，到最后，交换第一个数和最小数索引的数，从而把最小的数放到第一位

"""
o  -  -  -  -
*  o  -  -  -
*  *  o  -  -
*  *  *  o  -
*  *  *  *  o
"""

def select_sort(l):
    n = len(l)
    for j in range(n-1):
        min_index = j
        for i in range(1+j,n):                      # 未优化
            if l[i] < l[min_index]:
                min_index = i
        l[j],l[min_index] = l[min_index],l[j]
    return l

l = [2,4,1,5,7,8,3,5]

print(select_sort(l))



def select_sort(l):
    n =len(l)
    for j in range(0,n-1):                        # 被比较的数
        min = j
        for i in range(j+1,n):                    # 拿来比较的数
            if l[i] < l[min]:
                min = i
        l[min],l[j] = l[j],l[min]
    return l
print(select_sort(l))

