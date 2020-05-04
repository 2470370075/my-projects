# 堆排序： 将一个序列构建成大顶堆，然后把大顶和末尾数字交换，再构建成大顶堆，再交换，再构建，直到排好序。


#           第一次构建从后往前找父节点，调换顺序后，排它的子节点，
#           排好后调换顶层元素和末尾元素
#           第二次构建的时候，直接找最顶层的父节点，对剩余的树进行调换顺序，调换完后，排它的子节点，

#          最后一个根节点的索引是列表长度除2减1

# def shift(l,root,n):
#     while root <= n // 2 - 1:
#         child = 2 * root + 1
#         if child < n - 1 and l[child + 1] > l[child]:
#             child += 1
#         if l[child] > l[root]:
#             l[child],l[root] = l[root],l[child]
#         root = 2 * root + 1
#
# def heap_sort(l):
#     lenth = len(l)
#     index = len(l) - 1
#     root = lenth // 2 - 1
#     for i in range(root,-1,-1):
#         shift(l,i,lenth)
#     for j in range(index,0,-1):
#         l[0],l[j] = l[j],l[0]
#         shift(l,0,j)
#     return l
#
# l = [3, 1, 4, 9, 6, 7, 5, 8, 2, 10]
# print(heap_sort(l))


# def shift(l,root,lenth):
#     root = root
#     lenth = lenth
#     while root <= lenth // 2 - 1:
#         child = root * 2 + 1
#         if child + 1 <= lenth - 1 and l[child+1] > l[child]:
#             child += 1
#         if l[child] > l[root]:
#             l[child],l[root] = l[root],l[child]
#         root = root * 2 + 1
#
# def heap(l):
#     lenth = len(l)
#     root = lenth // 2 - 1
#     for i in range(root,-1,-1):
#         shift(l,i,lenth)
#     for j in range(lenth - 1,0,-1):
#         l[0],l[j] = l[j],l[0]
#         shift(l,0,j)
#     return l
#
# l = [3, 1, 4, 9, 6, 7, 5, 8, 2, 2]
#
# print(heap(l))
#

# def shift(l,root,lenth):
#     root = root
#     lenth = lenth
#     while root <= lenth // 2 - 1:
#         child = root * 2 + 1
#         if child + 1 <= lenth - 1 and l[child+1] > l[child]:
#             child += 1
#         if l[child] > l[root]:
#             l[child],l[root] = l[root],l[child]
#         root = root * 2 + 1
#
# def heap(l):
#     lenth = len(l)
#     root = lenth // 2 - 1
#     for i in range(root,-1,-1):
#         shift(l,i,lenth)
#     for j in range(lenth - 1,0,-1):
#         l[0],l[j] = l[j],l[0]
#         shift(l,0,j)
#     return l
#
# l = [3, 1, 4, 9, 6, 7, 5, 8, 2, 2]
#
# print(heap(l))



def shift(l,root,lenth):
    root = root
    lenth = lenth
    while root <= lenth // 2 - 1:
        child = root * 2 + 1
        if child + 1 <= lenth - 1 and l[child+1] > l[child]:
            child += 1
        if l[child] > l[root]:
            l[child],l[root] = l[root],l[child]
        root = child



def heap(l):
    lenth = len(l)
    root = lenth // 2 - 1
    for i in range(root,-1,-1):
        shift(l,i,lenth)
    for j in range(lenth - 1,0,-1):
        l[j],l[0] = l[0],l[j]
        shift(l,0,j)
    return l

import random
l = [3, 1, 4, 9, 6, 7, 5, 8, 2, 2]
random.shuffle(l)
print(l)
print(heap(l))












