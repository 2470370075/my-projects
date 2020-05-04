# 希尔排序：gap排序,分子序列

# 希尔排序: 插入排序的升级版，先取一个gap，
#           以0，0+gap，0+2gap，......为一个子序列，以1，1+gap，1+2gap......为一个子序列,
#           将整个序列划分为gap个子序列，分别进行插入排序
#           再减小gap的值
#           重新划分子序列，重新排序
#           直到gap为1，此时的序列是整个序列，排序完成后结束。


"""
×             ×             ×
    ×             ×
        ×             ×
            ×             ×
"""

def shell_sort(l):
    n = len(l)
    gap = n // 2
    while gap > 0:
        for i in range(n-gap):
            while i >= 0:
                if l[i+gap] < l[i]:
                    l[i],l[i+gap] = l[i+gap],l[i]
                    i -= gap
                else:
                    break
        gap = gap // 2
    return l

l = [1,4,2,3,6,4,8,5]
print(shell_sort(l))


def shell(l):
    n = len(l)
    gap = n // 2
    while gap > 0:
        for i in range(gap,n):
            while i > gap:
                if l[i] < l[i-gap]:
                    l[i],l[i-gap] = l[i-gap],l[i]
                    i -= gap
                else:
                    break
        gap = gap // 2
    return l


print(shell(l))














