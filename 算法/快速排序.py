
# low high夹逼排序

# 快速排序： 以最左面元素为low，最右面元素为high，并以low为中间值，
#           high如果比中间值大，正常，high = high - 1，如果小，不正常，放在low的位置，high = high - 1，
#           再去操作low，low如果比中间值小，正常，low = low + 1，如果大，不正常，放在high的位置，low = low + 1，
#           再去操作high，如此循环，当low=high时，再把中间值填进去，完成一次排序，
#           以中间值现在的位置为分界，将原序列划分成两个序列，分别递归，直到分完的子序列只含有一个元素，
#           快速排序完成

#    用到了递归，相当于返回了多个值  !! 此方法就用不了return了

"""
 - - - - - - -
 - - -   - - -
 -   -   -   -
"""
def quick_sort(l,first,last):
    if first >= last:
        return
    mid_value = l[first]
    low = first
    high = last
    while low < high:
        while low < high and l[high] >= mid_value:
            high -= 1
        l[low] = l[high]
        while low < high and l[low] < mid_value:
            low += 1
        l[high] = l[low]
    l[low] = mid_value
    quick_sort(l,first,low-1)
    quick_sort(l,low+1,last)

l = [5,2,3 ,4,6 ,8,4,3]
print(quick_sort(l,0,7))
print(l)


def quick(l,first,last):
    if first >= last:
        return
    low = first
    high = last
    mid_value = l[low]
    while low < high:
        while low < high and l[high] >= mid_value:
            high -= 1
        l[low] = l[high]
        while low < high and l[low] < mid_value:
            low += 1
        l[high] = l[low]
    l[low] =mid_value
    quick(l,first,low)
    quick(l,low+1,last)

l = [5,2,3 ,4,6 ,8,4,3]

print(quick(l,0,len(l)-1))
print(l)







def quick(l,first,last):
    if last <= first:
        return
    low = first
    high = last
    mid_value = l[low]
    while low < high:
        while low < high and l[high] >= mid_value:
            high -= 1
        l[low] = l[high]
        while low < high and l[low] <= mid_value:
            low += 1
        l[high] = l[low]
    l[low] = mid_value
    quick(l,first,low)
    quick(l,low+1,last)


l = [5,2,3 ,4,6 ,8,4,3]

print(quick(l,0,len(l)-1))
print(l)














